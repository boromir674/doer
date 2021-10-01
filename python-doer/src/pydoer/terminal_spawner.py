import os
import sys
from time import sleep

from .commands import CommandsBuilder, cmd


class ScriptGenerator:
    
    # PREDEFINED_COMMANDS = {
    #     'git': CommandsBuilder.subclasses['git'],
    #     'ipython': CommandsBuilder.subclasses['ipython'],
    #     'mpeta': CommandsBuilder.subclasses['mpeta'],
    # }
    
    # TERMINALS_CONFIG = {
    #     'git': lambda git_root: [cmd('cd', git_root), cd('arbitrary-command', 'git status')],
    #     'ipython': lambda working_directory, interpreter_version: [cmd('cd', working_directory), IPythonCommand(interpreter_version)],
    #     'mpeta': lambda commands_list: commands_list
    # }

    @staticmethod
    def create_script_file(file_path, commands):
        """Write each item in the commands list in a separate line in the file.

        Args:
            file_path (str): path to the destination file
            commands (list): list of strings
        """
        with open(file_path, 'w') as f:
            f.write('\n'.join(commands))

    @classmethod
    def create_rc_file(cls, terminal_type: str, target_path: str, *args, global_rc_file_path=''):
        """Create a script file, that holds the initially executed commands on a newly spawned terminal.
        
        This script is suitable to be executed to bootstrap a newly spawned terminal.

        Given the destination file path, the terminal type and an optional file to issue a 'source' command on,
        writes the shell script in a file.

        The script's commands are loaded from built-in commands in case the terminal type is 'git' or 'ipython'/
        In case of different terminal type, any commandsneed to be passed to this function through *args (positional arguments).

        Args:
            terminal_type (str): string representing the purpose (ie git, test) of the terminal to spawn
            target_path (str): path to the destination file
            global_rc_file_path (str, optional): [description]. Defaults to ''.
        """
        cls.create_script_file(
            target_path,
            cls._common_commands(
                terminal_type.upper(),
                global_rc_file_path=global_rc_file_path) + \
                CommandsBuilder.subclasses.get(terminal_type, CommandsBuilder.subclasses['mpeta']).build_commands(*args))
                # cls.PREDEFINED_COMMANDS.get(terminal_type, cls.PREDEFINED_COMMANDS.get('mpeta')).build_commands(*args))
                # cls.TERMINALS_CONFIG.get(terminal_type, cls.TERMINALS_CONFIG['mpeta'])(*args))

    @staticmethod
    def _common_commands(terminal_title, global_rc_file_path=''):
        """Create a list of strings, each of which represents a valid shell command on separate lines.

        The list of commands include
            1. a banshee string: !#/bin/bash
            2. (Optional) a command to "source" a file: eg source /path/to/.bashrc
            3. a command to change the terminal window title, as it appears in the window upper header

        Args:
            terminal_title (str): the title to use as the terminal's window title
            global_rc_file_path (str, optional): path to a file suitable to "source". Defaults to ''.

        Returns:
            list: list of strings each of which is a valid line representing a shell command
        """
        if os.path.isfile(global_rc_file_path):
            return ['#!/bin/bash', cmd('source', global_rc_file_path), cmd('set-terminal-title', terminal_title)]
        return ['#!/bin/bash', cmd('set-terminal-title', terminal_title)]
