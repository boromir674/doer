import os

import pytest

from pydoer.cli import menu


this_file_parent_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(params=[
    ['correct_menu_design', 0],
])
def menu_design_data(request, test_suite_data_dir):
    return type('TestMenuDesignData', (), {
        'menu_design_folder': os.path.join(test_suite_data_dir, request.param[0]),
        'expected_exit_code': request.param[1],
    })


def test_menu_design(menu_design_data, cli_runner):
    response = cli_runner.invoke(menu, [menu_design_data.menu_design_file])
    assert response.exit_code == menu_design_data.expected_exit_code
