import attr

from pydoer.common_terminal_commands import CommonCommands
from pydoer.doer_script_generator import DoerScriptGenerator
from pydoer.script_name import LaunchScriptPathFinder


@attr.s(slots=True)
class TerminalBootstrapScriptGenerator:
    task_name: str = attr.ib()
    output_dir: str = attr.ib()
    global_rc_file: str = attr.ib(default='')
    generator = attr.ib(init=False, default=None)
    path_finder = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        self.generator = DoerScriptGenerator(self.output_dir)
        self.path_finder = LaunchScriptPathFinder(self.output_dir)

    def generate(self, terminal_design):
        # create string 'commands' such as banshee string, cd to root dir, etc
        common_commands = CommonCommands.create('bash',
            terminal_design.window_title.upper(),
            self.global_rc_file,
            terminal_design.root
        )

        return self.generator.generate(
            '\n'.join(list(common_commands) + terminal_design.commands),
            self.path_finder.path(self.task_name, terminal_design.window_title)
        )
