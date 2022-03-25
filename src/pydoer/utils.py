from __future__ import annotations
import subprocess
from typing import List, Protocol, Callable

__all__ = ['find_open_windows']


class WindowType(Protocol):
    id: str
    title: str
    timestamp: str

    @staticmethod
    def from_wmctrl(window: str) -> WindowType: ...


WindowFactory = Callable[[str], WindowType]


def find_open_windows(window_factory: WindowFactory) -> List[WindowType]:
    """Find out what windows are currently 'open' in the OS.

    Returns:
        List[Window]: [description]
    """
    command_args = ('wmctrl',  '-lx')
    child_process = subprocess.run(list(command_args), capture_output=True, check=False)
    if child_process.returncode != 0:
        raise RuntimeError(f"Command '{' '.join(command_args)}' exited with non-zero status. "
                           f"Stderr: {child_process.stderr.decode().strip()}")
    return [window_factory(window_string) for window_string in child_process.stdout.decode().strip().split('\n')]
