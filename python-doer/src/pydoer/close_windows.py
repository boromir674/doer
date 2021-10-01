from typing import List
import subprocess

from .menu_creator import win_manager


def close_windows(windows_ids: List[str]):
    print('DEBUG: Windows IDs:', windows_ids)
    for window_id in windows_ids:
        print(f"Closing '{window_id}' window: {win_manager.windows[window_id].title}")
        child_process = subprocess.run(['wmctrl',  '-ic', window_id], capture_output=True)
        # if child_process.returncode != 0:

        # out, error = subprocess.Popen(['wmctrl',  '-ic', window_id], out=subprocess.STDOUT)


def close_spawned_windows():
    close_windows([win.id for win in win_manager.windows])


def main():
    close_spawned_windows()


if __name__ == '__main__':
    main()
