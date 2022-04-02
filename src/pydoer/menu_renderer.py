import os
import sys
from typing import Iterable

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from software_patterns import Observer

from .console_command import MyCommandItem
from .windows_manager_instance import windows_manager

from pydoer.doer_launcher_script_generator import TerminalBootstrapScriptGenerator
from pydoer.doer_task_script_generator import TaskScriptGenerator


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
        self._generate_task_script = TaskScriptGenerator(
            self._my_dir
        ).generate
        self._terminal_script_generator = TerminalBootstrapScriptGenerator(
            '',
            self._my_dir,
            self._doer_rc_file,
        )

    def get_menu(self, design_dir: str):
        options_dir = os.path.join(design_dir, 'options')
        task_files = [os.path.join(options_dir, x) for x in os.listdir(options_dir)]
        master_file = os.path.join(design_dir, 'menu.json')
        return self.construct_menu_1(task_files, master_file=master_file)

    def show(self):
        try:
            self.console_menu.show()
        except KeyboardInterrupt:
            print('\nExiting..')
            sys.exit(1)

    def construct_menu_1(self, task_files: Iterable[str], master_file=None):
        from pydoer.menu_factory import MenuFactory
        menu = MenuFactory.create(task_files, master_file=master_file)
        self.console_menu = ConsoleMenu(menu.title, menu.subtitle)
        
        # Create the Doer Menu options and bind commands
        for task in menu.item_tasks:
            script_path = self._create_do_script(task)
            command = MyCommandItem(task.name, 'bash {}'.format(script_path))
            command.subject.attach(self.terminal_spawn_listener)
            self.console_menu.append_item(command)

        # Create the last Doer Menu option, that closes opened windows
        self.console_menu.append_item(FunctionItem('Close Opened Windows', windows_manager.close_all))

    def _create_do_script(self, task):
        """Create a Task (aka Do) script.

        A task script, when executed, spawns one or more terminal applications.

        Args:
            task ([type]): [description]

        Returns:
            str: path of the shell script stored in the disk
        """
        self._terminal_script_generator.task_name = task.name
        
        # Generate Task (aka do) script
        do_script: str = self._generate_task_script(task)
        with open('/tmp/doer', 'w') as ff:
            ff.write(f'DO SCRIPT PATH: ' + str(do_script) + '\n')

        # Generate Terminal (aka launch) script(s)
        for terminal in task.terminal_designs:
            self._terminal_script_generator.generate(terminal)

        return do_script
