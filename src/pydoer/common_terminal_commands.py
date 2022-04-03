from software_patterns import SubclassRegistry

from pydoer.commands import cmd


class CommonCommands(list, metaclass=SubclassRegistry):
    pass


@CommonCommands.register_as_subclass('bash')
class BashCommonCommands(CommonCommands):

    def __new__(
        cls,
        terminal_title: str,
        global_rc_file_path: str = '',
        root_path: str = '',
        *args,
        **kwargs
    ):
        return list(filter(None, [
            '#!/bin/bash',
            cls._source_command(global_rc_file_path),
            cmd('set-terminal-title', terminal_title),
            cls._cd_command(root_path),
        ]))

    @classmethod
    def _source_command(cls, shell_script_file_path: str):
        """Get a Source Command instance; object that represents a "source /path/to/file" shell command.

        Args:
            shell_script_file_path (str): path to file to source
        """
        if shell_script_file_path != '':
            return cmd('source', shell_script_file_path)

    @classmethod
    def _cd_command(cls, path: str):
        if path != '':
            return cmd('cd', path)
