import os
import pytest


@pytest.fixture
def correct_menu_design(test_suite_data_dir):
    return os.path.join(test_suite_data_dir, 'correct_menu_design')


@pytest.fixture
def create_menu(correct_menu_design, scripts_dir):
    from pydoer.cli import menu_handler
    def _create_menu():
        return menu_handler(correct_menu_design, scripts_dir)
    return _create_menu


def test_menu(create_menu):
    menu = create_menu()
    assert menu
    assert hasattr(menu, 'show')
