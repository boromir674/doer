import subprocess
import attr

from pydoer.persistance import PersistanceManager
from .windows import Window


__all__ = ['win_manager']


@attr.s
class WindowsManager:
    """Store information about opened windows."""
    persistance: PersistanceManager = attr.ib(default=attr.Factory(PersistanceManager))
    windows: dict = attr.ib(default=attr.Factory(dict))  # last opened group of windows from single doer choice

    @classmethod
    def from_persist_file(cls, file_path: str):
        """Create an instance of WindowsManager given a custom file path to use for persistance (save/load).

        Factory method
        Args:
            file_path (str): the file that shall store informatin about windows opened by pydoer

        Returns:
            WindowsManager: an newly created instance of WindowsManager
        """
        return WindowsManager(PersistanceManager(file_path))

    def remember(self):
        """Store the lastly opend windows group in a persistant file and empty 'self.windows' dict."""
        self.persistance.save('\n'.join([Window.encode(window) for window in self.windows.values()]) + '\n')
        self.windows = {}

    def close_all(self):
        """Close all windows 'remembered' and those 'lastly opened', if any; then empty cache file."""
        windows = [Window.decode(window_string) for window_string in self.persistance.iter_windows()]
        for window in windows:
            print(f"Closing '{window.id}' window: {window.title}")
            # since check=False no exception is thrown if the wmctrl -ic command fails
            subprocess.run(['wmctrl',  '-ic', window.id], capture_output=True, check=False)
        self.persistance.flush()
