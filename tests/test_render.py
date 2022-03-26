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


def test_cli(menu_design_data, cli_runner):
    response = cli_runner.invoke(menu, [menu_design_data.menu_design_folder ])
    assert response.exit_code == menu_design_data.expected_exit_code


@pytest.fixture
def create_menu():
    from pydoer.menu_renderer import MenuRenderer
    class ToyListener:
        def update(self, *args, **kwargs):
            print('L')
    menu_renderer = MenuRenderer(
        ToyListener(),
    )
    options_dir = lambda x: os.path.join(x, 'options')
    return lambda design_root_dir: menu_renderer.construct_menu_1(
        [os.path.join(options_dir(design_root_dir), x) for x in os.listdir(options_dir(design_root_dir))],
        master_file=os.path.join(design_root_dir, 'menu.json')
    )


def test_menu_renderer(create_menu, menu_design_data):
    create_menu(
        menu_design_data.menu_design_folder
    )
