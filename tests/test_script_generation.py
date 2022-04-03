import os

import pytest


@pytest.fixture
def generate_terminal_script(tmp_path):
    from pydoer.doer_task_script_generator import TaskScriptGenerator
    from pydoer.task_design import TaskDesign
    from pydoer.terminal_design import TerminalDesign
    script_generator = TaskScriptGenerator(tmp_path)
    def generate_rc_script(commands, task_name, terminal_name):
        task_design = TaskDesign(task_name, None, [  # a task with 1 terminal spawned
            TerminalDesign(commands, None, terminal_name)
        ])
        return script_generator.generate(task_design)
    return generate_rc_script


@pytest.mark.parametrize('task_name, terminal_name, commands, script_content', (
    (
        'CV',
        'dev',
        [
            'echo "PYDOER TEST SUITE"',
            'echo "GOOD STUFF"'
        ],
        # expected do script contents
        'gnome-terminal -e "bash --rcfile {root_dir}/launch-CV-DEV.sh"\n'
        'wmctrl -r Terminal -N DEV'
    ),

))
def test_terminal_script_generation(
        commands,
        task_name,
        terminal_name,
        script_content,
        generate_terminal_script,
        tmp_path
    ):
    file_path = generate_terminal_script(
        commands,
        task_name,  # menu option
        terminal_name  # terminal
    )

    assert os.path.exists(file_path)
    
    with open(file_path, 'r') as do_script:
        contents = do_script.read()
    
    assert contents == script_content.format(root_dir=tmp_path)
