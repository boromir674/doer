import os
import sys
from time import sleep


class ScriptGenerator:

    TERMINALS_CONFIG = {
        'git': lambda git_root: [CdCommand(git_root), ArbitraryCommand('git status')],
        'ipython': lambda working_directory, interpreter_version: [CdCommand(working_directory), IPythonCommand(interpreter_version)],
        'mpeta': lambda commands_list: commands_list
    }

    @staticmethod
    def create_script_file(file_path, commands):
        with open(file_path, 'w') as f:
            f.write('\n'.join(commands))

    @classmethod
    def create_rc_file(cls, terminal_type, target_path, *args, global_rc_file_path=''):
        cls.create_script_file(target_path, cls._common_commands(terminal_type.upper(), global_rc_file_path=global_rc_file_path) + cls.TERMINALS_CONFIG.get(terminal_type, cls.TERMINALS_CONFIG['mpeta'])(*args))

    @staticmethod
    def _common_commands(terminal_title, global_rc_file_path=''):
        if os.path.isfile(global_rc_file_path):
            return ['#!/bin/bash', SourceCommand(global_rc_file_path), SetTerminalTitleCommand(terminal_title)]
        return ['#!/bin/bash', SetTerminalTitleCommand(terminal_title)]


class BashCommand(str):
    subclasses = {}

    def __new__(cls, *args, **kwargs):
        silence_all = kwargs.get('silence_all', False)
        run_in_background = kwargs.get('run_in_background', False)
        if hasattr(cls, '_text'):
            x = super().__new__(cls, cls._text.format(*args))
        else:
            x = super().__new__(cls, args[0])
        if silence_all:
            x += ' >/dev/null 2>&1'
        if run_in_background:
            x += ' &'
        return x

    @classmethod
    def register_subclass(cls, command_type):
        def decorator(subclass):
          cls.subclasses[command_type] = subclass
          return subclass
        return decorator

    @classmethod
    def create(cls, command_type, *args, **kwargs):
        if command_type not in cls.subclasses:
            raise ValueError('Bad command type {}'.format(command_type))
        return cls.subclasses[command_type](*args, **kwargs)



@BashCommand.register_subclass('arbitrary-command')
class ArbitraryCommand(BashCommand): pass

@BashCommand.register_subclass('spawn-terminal')
class SpawnTerminalCommand(BashCommand):
    _text = 'gnome-terminal -e "bash --rcfile {}"'

@BashCommand.register_subclass('set-terminal-title')
class SetTerminalTitleCommand(BashCommand):
    _text = 'set-title {}'

@BashCommand.register_subclass('cd')
class CdCommand(BashCommand):
    _text = 'cd {}'

@BashCommand.register_subclass('xdg-open')
class XdgOpenCommand(BashCommand):
    _text = 'xdg-open {}'

@BashCommand.register_subclass('ipython')
class IPythonCommand(BashCommand):
    _text = 'ipython{}'

@BashCommand.register_subclass('python3')
class Python3Command(BashCommand):
    _text = 'python3 {}'

@BashCommand.register_subclass('source')
class SourceCommand(BashCommand):
    _text = 'source {}'

@BashCommand.register_subclass('rename-terminal')
class WMCTRLCommand(BashCommand):
    _text = 'wmctrl -r Terminal -N {}'

@BashCommand.register_subclass('register-title-setter')
class RegisterTitleSetterCommand(BashCommand):
    _text = 'titlesette={}'

@BashCommand.register_subclass('git-timeline')
class GitTimelineCommand(BashCommand):
    _text = 'git log --graph --all --oneline --decorate | head -25'
