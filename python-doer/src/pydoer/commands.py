from .subclass_registry import SubclassRegistry


class BashCommand(str, metaclass=SubclassRegistry):
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

    # @classmethod
    # def register_subclass(cls, command_type):
    #     def decorator(subclass):
    #       cls.subclasses[command_type] = subclass
    #       return subclass
    #     return decorator

    # @classmethod
    # def create(cls, command_type, *args, **kwargs):
    #     if command_type not in cls.subclasses:
    #         raise ValueError('Bad command type {}'.format(command_type))
    #     return cls.subclasses[command_type](*args, **kwargs)


@BashCommand.register_as_subclass('arbitrary-command')
class ArbitraryCommand(BashCommand): pass

@BashCommand.register_as_subclass('spawn-terminal')
class SpawnTerminalCommand(BashCommand):
    _text = 'gnome-terminal -e "bash --rcfile {}"'

@BashCommand.register_as_subclass('set-terminal-title')
class SetTerminalTitleCommand(BashCommand):
    _text = 'set-title {}'

@BashCommand.register_as_subclass('cd')
class CdCommand(BashCommand):
    _text = 'cd {}'

@BashCommand.register_as_subclass('xdg-open')
class XdgOpenCommand(BashCommand):
    _text = 'xdg-open {}'

@BashCommand.register_as_subclass('ipython')
class IPythonCommand(BashCommand):
    _text = 'ipython{}'

@BashCommand.register_as_subclass('python3')
class Python3Command(BashCommand):
    _text = 'python3 {}'

@BashCommand.register_as_subclass('source')
class SourceCommand(BashCommand):
    _text = 'source {}'

@BashCommand.register_as_subclass('rename-terminal')
class WMCTRLCommand(BashCommand):
    _text = 'wmctrl -r Terminal -N {}'

@BashCommand.register_as_subclass('register-title-setter')
class RegisterTitleSetterCommand(BashCommand):
    _text = 'titlesette={}'

@BashCommand.register_as_subclass('git-timeline')
class GitTimelineCommand(BashCommand):
    _text = 'git log --graph --all --oneline --decorate | head -25'


cmd = BashCommand.create


class CommandsBuilder(metaclass=SubclassRegistry):
    @classmethod
    def build_commands(cls, *args, **kwargs) -> list:
        raise NotImplementedError


@CommandsBuilder.register_as_subclass('git')
class GitCommands(CommandsBuilder):
    @classmethod
    def build_commands(cls, *args, **kwargs):
        folder_to_navigate_to = args[0]
        return [cmd('cd', folder_to_navigate_to), cmd('arbitrary-command', 'git status')]


@CommandsBuilder.register_as_subclass('ipython')
class IpythonCommands(CommandsBuilder):
    @classmethod
    def build_commands(cls, *args, **kwargs):
        folder_to_navigate_to = args[0]
        python_interpreter_version = args[1]
        return [cmd('cd', folder_to_navigate_to), cmd('ipython', python_interpreter_version)]


@CommandsBuilder.register_as_subclass('mpeta')
class CustomCommands(CommandsBuilder):
    @classmethod
    def build_commands(cls, *args, **kwargs):
        commands_list = args[0]
        return commands_list
