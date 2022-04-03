from functools import reduce
from typing import Optional

import attr

from pydoer.commands import cmd
from pydoer.doer_script_generator import DoerScriptGenerator
from pydoer.script_name import LaunchScriptPathFinder, TaskScriptPathFinder


@attr.s
class TaskScriptGenerator:
    output_dir: str = attr.ib()

    script_generator: Optional[DoerScriptGenerator] = attr.ib(init=False, default=None)
    do_script_path_finder = attr.ib(init=False, default=None)
    launch_script_path_finder = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        self.script_generator = DoerScriptGenerator(self.output_dir)
        self.do_script_path_finder = TaskScriptPathFinder(self.output_dir)
        self.launch_script_path_finder = LaunchScriptPathFinder(self.output_dir)

    def generate(self, task_design):

        return self.script_generator.generate(
            '\n'.join(reduce(
                lambda i, j: i + j,
                    [
                        self.commands(task_design.name, terminal, rename=True)
                            for terminal in task_design.terminal_designs
                    ]
                )
            ),
            self.do_script_path_finder.path(task_design.name)
        )

    def commands(self, task_name: str, terminal, rename=True):
        return getattr(self, self.rename_map[rename])(*[
            self.launch_script_path_finder.path(
                task_name,
                terminal.window_title.upper()
            ),
            terminal.window_title.upper(),
        ])

    rename_map = {
        True: '_commands_with_rename',
        False: '_commands',
    }

    def _commands_with_rename(self, rc_file_path: str, title: str):
        return [
            self._spawn_terminal_cmd(rc_file_path),
            self._rename_terminal_window_cmd(title)
        ]
    
    def _commands(self, rc_file_path: str):
        return [
            self._spawn_terminal_cmd(rc_file_path),
        ]

    def _spawn_terminal_cmd(self, rc_file_path: str):
        """Shell command that can spawn a new terminal application.

        Call this method to get a shell command as a string. The command,
        when executed, can spawn a new terminal application.

        Example command that spawns a terminal on Debian Linux:

        gnome-terminal -e "bash --rcfile userrc"
        """
        return cmd('spawn-terminal', rc_file_path)

    def _rename_terminal_window_cmd(self, title: str):
        return cmd('rename-terminal', title)
