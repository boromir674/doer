#!/usr/bin/python3

import sys
import os
import re
import json
from consolemenu import *
from consolemenu.items import *

from functools import reduce

from src.terminal_spawner import ScriptGenerator, BashCommand

#
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


class MenuRenderer:
    _entries = []
    __my_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, doer_rc_file='', generated_scripts_directory=''):
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
                menu.append_item(CommandItem(menu_dict['label'], 'bash {}'.format(script_path)))
            try:
                menu.show()
            except KeyboardInterrupt:
                print('\nExiting..')
                sys.exit(1)

    def _create_bash_script(self, entry_data):
        script_path = self._path(entry_data['_id'])
        self._spawner.create_script_file(script_path,
                                         reduce(lambda i, j: i + j,
                                                [self._commands(entry_data['_id'], terminal_type, try_rename_again=True)
                                                 for terminal_type in [x['type'] for x in entry_data['terminals']]]
                                                ))
        for terminal_data in entry_data['terminals']:
            if 'commands' in terminal_data:
                arguments = [terminal_data['commands']]
                if 'root' in terminal_data:
                    arguments[0] = [BashCommand.create('cd', terminal_data['root'])] + arguments[0]
            else:
                arguments = [_ for _ in [terminal_data.get('root', None), terminal_data.get('interpreter_version', None)] if _]
            self._spawner.create_rc_file(terminal_data['type'], self._path(entry_data['_id'], launcher=terminal_data['type']), *arguments, global_rc_file_path=self._doer_rc_file)
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
            return [BashCommand.create('spawn-terminal', self._path(doer, launcher=terminal_type)),
                    BashCommand.create('rename-terminal', terminal_type.upper())]
        return [BashCommand.create('spawn-terminal', self._path(doer, launcher=terminal_type))]

class RoundTripEncoder(json.JSONEncoder): pass
    # def default(self, obj):
    #     return super().default(obj)

class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return obj


if __name__ == '__main__':
    mr = MenuRenderer(generated_scripts_directory='/data/tools/doer/python-doer/generated_bash_scripts')

    mr.construct_menu('/data/tools/doer/python-doer/menu_entries.json')
