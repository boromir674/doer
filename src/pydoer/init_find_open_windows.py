from .utils import find_open_windows
from .windows import build_find_open_windows

__all__ = ['find_open_windows']


find_open_windows = build_find_open_windows(find_open_windows)
