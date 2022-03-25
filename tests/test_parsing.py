import pytest


@pytest.fixture
def menu_design_factory_method():
    from pydoer.menu_factory import MenuFactory
    return MenuFactory.create


def test_menu_design(
    menu_design_factory_method,
    valid_menu_design_dir,
):
    menu_design = menu_design_factory_method(valid_menu_design_dir)
    assert [option.name for option in menu_design.options] == [
        'So Magic',
        'Option 2',
        'Option 3',
    ]
