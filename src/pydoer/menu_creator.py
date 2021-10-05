#!/usr/bin/env python

import os
import sys
import json
from time import sleep
import subprocess
from typing import List
from functools import reduce

import attr
import click
from consolemenu import *
from consolemenu import ConsoleMenu
from consolemenu.items import CommandItem

from .terminal_spawner import ScriptGenerator
from .commands import cmd
from .notification import *
from .windows import find_open_windows,Window




my_dir = os.path.dirname(os.path.realpath(__file__))
persist_file_name = '.windows_opened_by_doer.txt'

bash_scripts_dir_path = os.path.join(my_dir, 'generated_bash_scripts')


@attr.s
class PersistanceManager:
    cache_file: str = attr.ib(default=os.path.join(my_dir, persist_file_name))

    def save(self, string):
        with open(self.cache_file, 'a') as f:
            f.write(string + '\n')

    def read(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return f.read()
        else:
            return ''

    def iter_windows(self):
        windows_string = self.read()
        for line in windows_string.split('\n'):
            if line:
                yield line
            elif line == '':
                continue
            else:
                raise RuntimeError(f"Wierd formmated line: {line}")

    def flush(self):
        """Remove windows 'remembered' in the cache file."""
        with open(self.cache_file, 'w') as f:
            pass


@attr.s
class WindowsManager:
    """Store information about opened windows.
    """
    persistance = attr.ib(default=attr.Factory(PersistanceManager))
    windows = attr.ib(default=attr.Factory(dict))  # last opened group of windows from single doer choice

    @classmethod
    def from_persist_file(cls, file_path: str):
        """Create an instance of WindowsManager given a custom file path to use for persistance (save/load).
        
        Factory method 
        Args:
            file_path (str): the file that shall store informatin about windows opened by pydoer

        Returns:
            WindowsManager: an newly created instance of WindowsManager
        """
        return WindowsManager(PersistanceManager(file_path))

    def remember(self):
        """Store the lastly opend windows group in a persistant file and empty 'self.windows' dict."""
        self.persistance.save('\n'.join([Window.encode(window) for window in self.windows.values()]) + '\n')
        self.windows = {}

    def close_all(self):
        """Close all windows 'remembered' and those 'lastly opened', if any; then empty cache file."""
        windows = [Window.decode(window_string) for window_string in self.persistance.iter_windows()]
        for window in windows:
            print(f"Closing '{window.id}' window: {window.title}")
            child_process = subprocess.run(['wmctrl',  '-ic', window.id], capture_output=True)
        self.persistance.flush()


win_manager = WindowsManager()


@attr.s
class SpawnListener(Observer):
    windows_manager: WindowsManager = attr.ib(default=attr.Factory(WindowsManager))
    
    def update(self, *args, **kwargs) -> None:
        windows = args[0].state
        # replace all stored windows with the newly "observed" ones
        self.windows_manager.windows = {window.id: window for window in windows}
        self.windows_manager.remember()


class MyCommandItem(CommandItem):
    def __init__(self, text, command, arguments=None, menu=None, should_exit=False, subject=None):
        super().__init__(text, command, arguments=arguments, menu=menu, should_exit=should_exit)
        self.subject = subject if subject is not None else Subject()

    def action(self):
        # Before we execute the command we find out the currently open windows
        windows = find_open_windows()
        if windows is None:
            raise RuntimeError
        super().action()

        # todo measure time here
        # and noti'fy of newly spawned windows on another event to avoid sleeping immediately here
        # in other words do a lazy notification to avoid sleeping here
        sleep(2.0)

        windows_after = find_open_windows()
        if windows is None:
            raise RuntimeError

        nb_new_windows = len(windows_after) - len(windows)
        assert nb_new_windows > 0
        assert all([x == windows_after[i] for i, x in enumerate(windows)])
        new_windows = windows_after[-nb_new_windows:]
        self.subject.state = new_windows
        self.subject.notify()


class MenuRenderer:
    _entries = []
    __my_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, terminal_spawn_listener, doer_rc_file='', generated_scripts_directory=''):
        self.terminal_spawn_listener = terminal_spawn_listener
        if not doer_rc_file:
            doer_rc_file = os.path.join(self.__my_dir, 'doerrc')
        if not os.path.isfile(doer_rc_file):
            raise ValueError("Doer rc file '{}' is not a file".format(doer_rc_file))
        self._doer_rc_file  = doer_rc_file
        if generated_scripts_directory:
            self._my_dir = generated_scripts_directory
        else:
            self._my_dir = self.__my_dir
        self._spawner = ScriptGenerator()

    def construct_menu(self, json_file):
        with open(json_file, 'r') as fp:
            res = json.load(fp, cls=RoundTripDecoder)
            menu = ConsoleMenu(res['title'], res['subtitle'])
            for menu_dict in res['menu_entries']:
                script_path = self._create_bash_script(menu_dict)
                menu.append_item(MyCommandItem(menu_dict['label'], 'bash {}'.format(script_path)))
                item = menu.items[-1]
                item.subject.attach(self.terminal_spawn_listener)
            try:
                menu.show()
            except KeyboardInterrupt:
                print('\nExiting..')
                sys.exit(1)

    def _create_bash_script(self, entry_data):
        """Create a 'do' shell script.

        A 'do' script, when executed, spawns one or more terminal applications.

        Args:
            entry_data ([type]): [description]

        Returns:
            str: path of the shell script stored in the disk
        """
        script_path = self._path(entry_data['_id'])
        # create script that spawns a new terminal, upon execution
        self._spawner.create_script_file(script_path,
                                         reduce(lambda i, j: i + j,
                                                [self._commands(entry_data['_id'], terminal_type, try_rename_again=True)
                                                 for terminal_type in [x['type'] for x in entry_data['terminals']]]
                                                ))
        for terminal_data in entry_data['terminals']:
            if 'commands' in terminal_data:
                arguments = [terminal_data['commands']]
                if 'root' in terminal_data:
                    arguments[0] = [cmd('cd', terminal_data['root'])] + arguments[0]
            else:
                if terminal_data['type'] not in ('git' 'ipython'):
                    arguments = [[cmd('cd', terminal_data['root'])]]
                else:
                    arguments = [_ for _ in [terminal_data.get('root', None), terminal_data.get('interpreter_version', None)] if _]
            # Create script that should run on a newly spawned terminal. This script acts a step to setup the terminal
            self._spawner.create_rc_file(terminal_data['type'], self._path(entry_data['_id'],
                launcher=terminal_data['type']), *arguments, global_rc_file_path=self._doer_rc_file)
        return script_path

    def _path(self, doer, launcher=''):
        if launcher:
            return os.path.join(self._my_dir, 'launch-{}-{}.sh'.format(doer, launcher))
        return os.path.join(self._my_dir, 'do-{}.sh'.format(doer))

    def _commands(self, doer, terminal_type, try_rename_again=False):
        """
        Call this method to get a list of Bash commands:\n
        'gnome-terminal -e "bash --rcfile doer-specific-rcfile"'\n
        'set-title TERMINAL_TYPE'\n
        if rename is try_rename_again is True, or\n
        'gnome-terminal -e "bash --rcfile doer-specific-rcfile"'\n
        if rename is try_rename_again is False\n\n
        WARNING this method requires the set-title global bash function\n
        :param str doer:
        :param str terminal_type:
        :param bool try_rename_again:
        :return:
        :rtype: list
        """
        if try_rename_again:
            return [cmd('spawn-terminal', self._path(doer, launcher=terminal_type)),
                    cmd('rename-terminal', terminal_type.upper())]
        return [cmd('spawn-terminal', self._path(doer, launcher=terminal_type))]


class RoundTripEncoder(json.JSONEncoder): pass


class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return obj


@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
def close_doing():
    click.echo('CLOSE DOING')
    win_manager.close_all()


@cli.command()  # @cli, not @click!
@click.argument('json_path')  # help='path to the json file from which to construct the menu')
@click.option('-sd', '--scripts-dir', default=bash_scripts_dir_path, help='define your custom location to store the generated bash files')
def menu(json_path, scripts_dir):
    if not os.path.isdir(scripts_dir):
        try:
            os.makedirs(scripts_dir)
        except Exception as e:
            print(e)
            print('You can try the following:\n'
                  '* install pydoer in a location that the code will have permission to create a directory (eg using the --user flag with pip install\n'
                  '* pass in a directory using parameter flag -sd or --scripts-dir, where the code will have the necessary permissions to read/write')
            sys.exit(1)

    terminal_spawn_listener = SpawnListener(win_manager)

    mr = MenuRenderer(
        terminal_spawn_listener=terminal_spawn_listener,
        generated_scripts_directory=scripts_dir
    )
    mr.construct_menu(json_path)


if __name__ == '__main__':
    cli()





# LEGACY CODE


# # Create the menu
# menu = ConsoleMenu("DOER", "Do it, do it now!")
#
# # Create some items
#
# # MenuItem is the base class for all items, it doesn't do anything when selected
# menu_item = MenuItem("Menu Item")
#
# # A FunctionItem runs a Python function when selected
# function_item = FunctionItem("Call a Python function", input, ["Enter an input "])
#
# # A CommandItem runs a console command
# command_item = CommandItem("Run a console command",  "touch hello.txt")
#
# # A SelectionMenu constructs a menu from a list of strings
# selection_menu = SelectionMenu(["item1", "item2", "item3"])
#
# # A SubmenuItem lets you add a menu (the selection_menu above, for example)
# # as a submenu of another menu
# submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
#
# # Once we're done creating them, we just add the items to the menu
# menu.append_item(menu_item)
# menu.append_item(function_item)
# menu.append_item(command_item)
# menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
