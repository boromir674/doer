import os

import pytest
from click.testing import CliRunner

from pydoer.menu_creator import menu


this_file_parent_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(params=[
    [os.path.join(this_file_parent_dir, '..', 'menu_entries.json'), 0],
    [os.path.join(this_file_parent_dir, 'invalid-menu-entries-1.json'), 1],
    ])
def menu_design_data(request):
    return type('TestMenuDesignData', (), {
        'menu_design_file': request.param[0],
        'expected_exit_code': request.param[1],
    })

runner = CliRunner()


def test_menu_design(menu_design_data):
    response = runner.invoke(menu, [menu_design_data.menu_design_file])
    assert response.exit_code == menu_design_data.expected_exit_code
