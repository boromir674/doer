import os

import pytest


@pytest.fixture
def generate_file():
    from pydoer.terminal_spawner import ScriptGenerator
    return ScriptGenerator.create_script_file


@pytest.mark.parametrize('commands, script_content', (
    (
        (
            'echo "PYDOER TEST SUITE"',
            'echo "GOOD STUFF"'
        ),
        'echo "PYDOER TEST SUITE"\n'
        'echo "GOOD STUFF"'
    ),

    (
        (

        ),
        ''
    ),
))
def test_file_generation(commands, script_content, generate_file, tmp_path):
    file_path = os.path.join(tmp_path, 'test_terminal_script')
    generate_file(file_path, commands)
    assert os.path.exists(file_path)

    with open(file_path, 'r') as script_file:
        contents = script_file.read()
    assert contents == script_content
