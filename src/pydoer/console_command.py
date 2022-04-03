from time import sleep

from consolemenu.items import CommandItem
from software_patterns import Subject

from .init_find_open_windows import find_open_windows


# Item class that when selected executes an external script (ie bash)
class MyCommandItem(CommandItem):
    def __init__(self, text, command, subject=None):
        super().__init__(text, command)
        self.subject = subject if subject is not None else Subject()

    def action(self):
        # Before we execute the command we find out the currently open windows
        windows = find_open_windows()
        if windows is None:
            raise RuntimeError
        super().action()

        # todo measure time here
        # and notify of newly spawned windows on another event to avoid sleeping immediately here
        # in other words do a lazy notification to avoid sleeping here
        sleep(2.0)

        windows_after = find_open_windows()

        nb_new_windows = len(windows_after) - len(windows)
        nb_old_windows = len(windows)
        assert nb_new_windows > 0
        assert all((x == windows_after[i] for i, x in enumerate(windows)))
        # new_windows = windows_after[-nb_new_windows:]
        new_windows = windows_after[nb_old_windows:]
        self.subject.state = new_windows
        self.subject.notify()
