from typing import List
import subprocess
import re

import attr


__all__ = ['Window']


@attr.s
class Window:
    """Represents an open (running) window.

    Args:
        id (str): a unique string representing the id of the window
        title (str): the title of the window, that is displayed on the window's "menu bar" at the top
        timestamp (int, optional): the timestamp on which the window was first opened. Defaults to ''.
    """
    id: str = attr.ib()
    title: str = attr.ib()
    timestamp: str = attr.ib(default='')

    @classmethod
    def from_wmctrl(cls, window: str):
        matched_id, matched_window_title = re.match(r'^(.+?)[\ \t]+.+?[\ \t]+.+?[\ \t]+.+?[\ \t]+(.+)$', window).groups()
        # return list(re.match(r'^(0x[\d\w]+)[\t\ ]+[\ .:\-\w\d,]+[\t\ ]+([\w\-]+)$', window).groups())
        return Window(matched_id, matched_window_title)

    ## Encode/Decode functionality
    SPLIT = ' --> '
    
    @classmethod
    def encode(cls, window) -> str:
        return f'{window.id}{cls.SPLIT}{window.title}'

    @classmethod
    def decode(cls, window_string: str):
        """Construct a new Window instance from a string.

        Args:
            window_string (str): [description]

        Returns:
            Window: the new Window instance
        """
        return Window(*list(window_string.split(cls.SPLIT)))
    ##

    def __eq__(self, o: object) -> bool:
        return self.id == o.id


def find_open_windows() -> List[Window]:
    """Find out what windows are currently 'open' in the OS.

    Returns:
        List[Window]: [description]
    """
    command_args = ['wmctrl',  '-lx']
    child_process = subprocess.run(command_args, capture_output=True)
    if child_process.returncode != 0:
        raise RuntimeError(f"Invokation of command '{' '.join(command_args)}' exited with non-zero status.")
    return [Window.from_wmctrl(window_string) for window_string in child_process.stdout.decode().strip().split('\n')]


if __name__ == '__main__':
    print(find_open_windows())
