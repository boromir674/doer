import os
import sys
import click

from .windows_manager_instance import windows_manager
from .menu_renderer import MenuRenderer
from .window_spawn_listener import SpawnListener

import logging
logger = logging.getLogger(__name__)


MY_DIR = os.path.dirname(os.path.realpath(__file__))
bash_scripts_dir_path = os.path.join(MY_DIR, 'generated_bash_scripts')



@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
def close_doing():
    click.echo('CLOSE DOING')
    windows_manager.close_all()


@cli.command()  # @cli, not @click!
@click.argument('json_path')  # help='path to the json file from which to construct the menu')
@click.option('-sd', '--scripts-dir', default=bash_scripts_dir_path,
    help='define your custom location to store the generated bash files')
def menu(json_path, scripts_dir):
    logger.info('CLI is running!')
    menu_renderer = menu_handler(json_path, scripts_dir)
    menu_renderer.show()


def menu_handler(directory_path, scripts_dir):
    print('\n----------------\n')
    print('ARG1', f'"{directory_path}"')
    print('ARG2', f'"{scripts_dir}"')
    print('\n----- DEBUG cli', scripts_dir)
    if not os.path.isdir(scripts_dir):
        print('SCRIPTS DIR DOES NOT EXISTS')
        try:
            os.makedirs(scripts_dir)
        except Exception as any_exception:
            print(any_exception)
            print('You can try the following:\n'
                  '* install pydoer in a location that the code will have permission to create a directory '
                  '(eg using the --user flag with pip install\n'
                  '* pass in a directory using parameter flag -sd or --scripts-dir, where the code will have '
                  'the necessary permissions to read/write')
            sys.exit(1)

    terminal_spawn_listener = SpawnListener(windows_manager)
    
    menu_renderer = MenuRenderer(
        terminal_spawn_listener=terminal_spawn_listener,
        scripts_directory=scripts_dir
    )
    menu_renderer.get_menu(directory_path)
    return menu_renderer


if __name__ == '__main__':
    cli()
