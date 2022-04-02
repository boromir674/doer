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


"""        runner: "CliRunner",
        stdout_bytes: bytes,
        stderr_bytes: t.Optional[bytes],
        return_value: t.Any,
        exit_code: int,
        exception: t.Optional[BaseException],
        exc_info: t.Optional[
            t.Tuple[t.Type[BaseException], BaseException, TracebackType]
        ] = None,
    ):"""

def test_cli(menu_design_data, cli_runner, scripts_dir):
    response = cli_runner.invoke(menu, [menu_design_data.menu_design_folder, '--scripts-dir', scripts_dir])
    print('\nSTDOUT\n', str(response.stdout_bytes, encoding='utf-8'))
    if hasattr(response, 'stderr_bytes') and response.stderr_bytes:
        print(type(response.stderr_bytes))
        print('\nSTDERR\n', str(response.stderr_bytes, encoding='utf-8'))
    print('\nSTDEXIT_CODE\n', str(response.exit_code))
    print('\nEXCEPTION\n', str(response.exception))
    print('\nEXCEPTION_INFO\n', str(response.exc_info))
    assert response.exit_code == menu_design_data.expected_exit_code


@pytest.fixture
def create_menu(scripts_dir):
    from pydoer.menu_renderer import MenuRenderer
    class ToyListener:
        def update(self, *args, **kwargs): pass
    menu_renderer = MenuRenderer(
        ToyListener(),
        scripts_directory=scripts_dir,
    )
    return menu_renderer.get_menu


def test_menu_renderer(create_menu, menu_design_data, scripts_dir):
    create_menu(
        menu_design_data.menu_design_folder
    )
    assert os.path.exists(os.path.join(scripts_dir, 'do-So-Magic.sh'))
    assert os.path.exists(os.path.join(scripts_dir, 'do-Option-2.sh'))
    assert os.path.exists(os.path.join(scripts_dir, 'do-Option-3.sh'))
    assert os.path.exists(os.path.join(scripts_dir, 'launch-Option-3-SO_MAGIC_DEV.sh'))
    assert os.path.exists(os.path.join(scripts_dir, 'launch-So-Magic-SO_MAGIC_DEV.sh'))
