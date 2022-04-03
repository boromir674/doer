import os

import pytest


@pytest.fixture
def generate_file(tmp_path):
    from pydoer.doer_script_generator import DoerScriptGenerator
    script_generator = DoerScriptGenerator(tmp_path)
    return lambda file_name, iter_commands: script_generator.generate('\n'.join(iter_commands), file_name)


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
    file_path = generate_file('test_terminal_script', commands)
    assert os.path.exists(file_path)

    with open(file_path, 'r') as script_file:
        contents = script_file.read()
    assert contents == script_content
