import os
import sys
import json
from functools import reduce
from typing import Iterable

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from software_patterns import Observer

from .commands import cmd
from .console_command import MyCommandItem
from .terminal_spawner import ScriptGenerator
from .windows_manager_instance import windows_manager
from .menu_config import MenuConfig


class MenuRenderer:
    __my_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, terminal_spawn_listener: Observer, doer_rc_file='', scripts_directory=''):
        """A parser or terminal application(s) configuration (json) file and renderer of an interactive cli menu.

        Creates an instance of MenuRenderer given a "listener" that should know how to handle notification events, when
        a menu option is "selected".

        For each menu option, it generates a "do" script which is responsible then to spawn one or more terminal
        applications. Each terminal application will execute a common "doerrc" bash script that serves the same purpose
        of a ~/.bashrc file (ie login script). Then it runs the custom commands tailored to that terminal.

        Optionally, you can provide a "doerrc" script at runtime with the `doer_rc_file` kwarg or let the default run.
        Optionally, you can provide the location to store every automatically generated shell script (ie for debug).

        Args:
            terminal_spawn_listener (Observer): an object with an 'update' method that can handle newly observed windows
            doer_rc_file (str, optional): file that acts similarly to a ~/.bashrc file. Defaults to ''.
            scripts_directory (str, optional): the location to store the dynamically generated scripts. Defaults to ''.

        Raises:
            ValueError: [description]
        """
        self.terminal_spawn_listener = terminal_spawn_listener
        if not doer_rc_file:
            doer_rc_file = os.path.join(self.__my_dir, 'doerrc')
        if not os.path.isfile(doer_rc_file):
            raise ValueError("Doer rc file '{}' is not a file".format(doer_rc_file))
        self._doer_rc_file  = doer_rc_file
        if scripts_directory:
            self._my_dir = scripts_directory
        else:
            self._my_dir = self.__my_dir
        self._spawner = ScriptGenerator()

    def construct_menu(self, json_file):
        menu = MenuConfig.from_json_file(json_file)
        with open(json_file, 'r') as file_:
            res = json.load(file_, cls=json.JSONDecoder)
            console_menu = ConsoleMenu(res['title'], res['subtitle'])

            # Create the Doer Menu options, one per item in the design json
            for menu_dict in res['menu_entries']:
                script_path = self._create_bash_script(menu_dict)
                console_menu.append_item(MyCommandItem(menu_dict['label'], 'bash {}'.format(script_path)))
                item = console_menu.items[-1]
                item.subject.attach(self.terminal_spawn_listener)

            # Create the last Doer Menu option, that closes opened windows
            console_menu.append_item(FunctionItem('Close Opened Windows', windows_manager.close_all))

            try:
                console_menu.show()
            except KeyboardInterrupt:
                print('\nExiting..')
                sys.exit(1)

    def construct_menu_1(self, task_files: Iterable[str], master_file=None):
        from pydoer.menu_factory import MenuFactory
        menu = MenuFactory.create(task_files, master_file=master_file)
        self.console_menu = ConsoleMenu(menu.title, menu.subtitle)
        
        # Create the Doer Menu options and bind commands
        for task in menu.item_tasks:
            script_path = self._create_bash_script(task)
            command = MyCommandItem(task.name, 'bash {}'.format(script_path))
            command.subject.attach(self.terminal_spawn_listener)
            self.console_menu.append_item(command)

        # Create the last Doer Menu option, that closes opened windows
        self.console_menu.append_item(FunctionItem('Close Opened Windows', windows_manager.close_all))

    def show(self):
        try:
            self.console_menu.show()
        except KeyboardInterrupt:
            print('\nExiting..')
            sys.exit(1)

    def _create_bash_script(self, entry_data):
        """
        Create a task bash script.

        A task script, when executed, spawns one or more terminal applications.

        Args:
            entry_data ([type]): [description]

        Returns:
            str: path of the shell script stored in the disk
        """
        script_path = self._path(entry_data.name)
        # create a script that holds one or more commands that spawn a new
        # terminal application (spawn commands)
        self._spawner.create_script_file(script_path,
                                         reduce(lambda i, j: i + j,
                                                [self._commands(entry_data.name, terminal.window_title, try_rename_again=True)
                                                 for terminal in entry_data.terminal_designs]
                                                ))
        for terminal in entry_data.terminal_designs:
            arguments = [[cmd('cd', terminal.root)] + terminal.commands]
            # Create a 'launch' script that should run on a newly spawned terminal.
            # each spawn command instructs the new terminal to initially run
            # a 'launch' script (rc file)
            self._spawner.create_rc_file(terminal.window_title, self._path(entry_data.name,
                launcher=terminal.window_title), *arguments, global_rc_file_path=self._doer_rc_file)
        return script_path

    def _path(self, doer, launcher=''):
        if launcher:
            # sub task (in dedicated terminal) of a menu option (task)
            return os.path.join(self._my_dir, 'launch-{}-{}.sh'.format(doer, launcher))
        # return a task script file path
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
