import os

import pytest
from click.testing import CliRunner

from pydoer.menu_creator import menu


this_file_parent_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def menu_designs():
    return {  # key -> (menu_file_path.json, expected_exit_code when exectuting the 'menu' command of the pydoer cli)
        'ko': (os.path.join(this_file_parent_dir, '..', 'menu_entries.json'), 0),
        'invalid-menu-1': (os.path.join(this_file_parent_dir, 'invalid-menu-entries-1.json'), 1),
    }


@pytest.fixture(params=[
    ['ko'],
    ['invalid-menu-1'],
    ])
def menu_design_data(request, menu_designs):
    return {
        'key': request.param[0],
        'menu_design_file': menu_designs[request.param[0]][0],
        'expected_exit_code': menu_designs[request.param[0]][1],
    }

runner = CliRunner()


def test_menu_design(menu_design_data):
    response = runner.invoke(menu, [menu_design_data['menu_design_file']])
    assert response.exit_code == menu_design_data['expected_exit_code']
