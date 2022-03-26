import os
import pytest


@pytest.fixture
def rc_script_file_path(tmp_path):
    def get_file_path(option_name: str, task_name: str):
        return os.path.join(tmp_path, f'do-{option_name}-{task_name}.sh')
    return get_file_path


@pytest.fixture
def generate_terminal_script(rc_script_file_path):
    from pydoer.terminal_spawner import ScriptGenerator
    def generate_rc_script(commands, option_name, task_name):
        file_path = rc_script_file_path(option_name, task_name)
        ScriptGenerator.create_rc_file(
            task_name, file_path, commands
        )
        return file_path
    return generate_rc_script


@pytest.mark.parametrize('commands, option_name, task_name, script_content', (
    (
        [
            'echo "PYDOER TEST SUITE"',
            'echo "GOOD STUFF"'
        ],
        'CV',
        'dev',
        '#!/usr/bin/env bash\n'
        'echo "PYDOER TEST SUITE"\n'
        'echo "GOOD STUFF"'
    ),

))
def test_terminal_script_generation(
        commands,
        option_name,
        task_name,
        script_content,
        generate_terminal_script
    ):
    file_path = generate_terminal_script(
        commands,
        option_name,  # menu option
        task_name  # terminal
    )
    assert os.path.basename(file_path) == f'do-{option_name}-{task_name}.sh'
    assert os.path.exists(file_path)
    
    with open(file_path, 'r') as do_script:
        contents = do_script.read()
    
    assert contents == script_content
