from .windows import Window


def build_find_open_windows(find_open_windows):
    return lambda: find_open_windows(Window.from_wmctrl)
