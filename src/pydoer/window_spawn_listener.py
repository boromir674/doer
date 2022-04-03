from typing import Protocol

import attr
from software_patterns import Observer


class WindowManagerProtocol(Protocol):
    windows: dict

    def remember(self) -> None: ...
 

@attr.s
class SpawnListener(Observer):
    windows_manager: WindowManagerProtocol = attr.ib()

    def update(self, *args, **kwargs) -> None:
        windows = args[0].state
        # replace all stored windows with the newly "observed" ones
        self.windows_manager.windows = {window.id: window for window in windows}
        self.windows_manager.remember()
