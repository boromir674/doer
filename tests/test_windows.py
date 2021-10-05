import pytest


@pytest.fixture
def window():
    from pydoer.windows import Window, find_open_windows
    return type('WindowsModule', (), {
        '_class': Window,
        'find_open_windows': find_open_windows,
    })
    
    # def _window():
    #     return Window.from_wmctrl('0x12345 0 wm_class_name_1 host window_title_A')


@pytest.mark.parametrize('wmctrl_line, expected_id, expected_title', [
    ('0x12345 0 wm_class_name_1 host window_title_A', '0x12345', 'window_title_A'),
    ('0x05000001  0 code.Code             dinos-Yoga-Slim-7-Pro-14ACH5-O ● test_windows.py - doer - Visual Studio Code', '0x05000001', '● test_windows.py - doer - Visual Studio Code'),
    ('0x04e00421  0 gnome-terminal-server.Gnome-terminal  dinos-Yoga-Slim-7-Pro-14ACH5-O GIT', '0x04e00421', 'GIT'),
    ('0x05c000a6  0 brave-browser.Brave-browser  dinos-Yoga-Slim-7-Pro-14ACH5-O wmctrl(1) - Linux man page - Brave', '0x05c000a6', 'wmctrl(1) - Linux man page - Brave')
])
def test_string_to_window(wmctrl_line, expected_id, expected_title, window):
    window = window._class.from_wmctrl(wmctrl_line)
    assert window.id == expected_id
    assert window.title == expected_title


def test_window_comparison(window):
    w1 = window._class('123', 'Title-A')
    w2 = window._class('123', 'Epilogue')
    assert w1 == w2

    w3 = window._class('0x123', 'Epilogue')
    assert w2 != w3


def test_find_windows(monkeypatch, window):
    # TODO build a mock of the output of a sucessful wmctrl -lx command
    import subprocess
    mocked_suceeded_wmctrl_child_process = type('MockedSuceededWmctrlChildProcess', (), {
        'returncode': 0,
        'stdout': b'0x12345 0 wm_class_name_1 host window_title_A\n0x05c000a6  0 brave-browser.Brave-browser  dibou-laptop-Slim-9-Pro-11BYU9-O wmctrl(1) - Linux man page - Brave\n',
        'stderr': b'',
    })
    def get_emulated_child_process(*args, **kwargs):
        return mocked_suceeded_wmctrl_child_process

    monkeypatch.setattr(subprocess, 'run', get_emulated_child_process)
    open_windows = window.find_open_windows()
    assert type(open_windows) == list
    print(open_windows)


# def test_encode


# def test_decode