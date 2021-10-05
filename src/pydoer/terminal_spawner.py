import os
from typing import List, Union
import sys
from time import sleep

from .commands import CommandsBuilder, cmd, BashCommand

source_command_type = Union[BashCommand, None]


class ScriptGenerator:

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
            list(cls._common_commands(
                terminal_type.upper(),
                global_rc_file_path=global_rc_file_path)) + \
                CommandsBuilder.subclasses.get(terminal_type, CommandsBuilder.subclasses['mpeta']).build_commands(*args))

    @classmethod
    def _common_commands(cls, terminal_title, global_rc_file_path=''):
        """Create shell commands that are common for all 'launch-scripts'

        Creates a list of strings, each of which represents a valid shell command when put on separate lines
        in a file script.

        The list of commands include
            1. a banshee string: !#/bin/bash
            2. a command to change the terminal window title, as it appears in the window upper header

        Args:
            terminal_title (str): the title to use as the terminal's window title
            global_rc_file_path (str, optional): path to a file suitable to "source". Defaults to ''.

        Returns:
            list: list of strings each of which is a line representing a valid shell command
        """
        return filter(None, ['#!/bin/bash', cls._source_command(global_rc_file_path), cmd('set-terminal-title', terminal_title)])

    def _source_command(shell_script_file_path: str) -> source_command_type:
        """Get a Source Command instance; object that represents a "source /path/to/file" shell command.

        Args:
            shell_script_file_path (str): path to file to source

        Returns:
            source_command_type: [description]
        """
        if os.path.isfile(shell_script_file_path):
            return cmd('source', shell_script_file_path)
