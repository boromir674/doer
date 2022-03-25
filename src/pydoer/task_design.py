"""Module for representing a user design for a task (menu option)."""

from typing import Dict, Iterable, Protocol, Optional
import attr


class TerminalDesignType(Protocol):
    commands: Optional[Iterable[str]]
    title: Optional[str]
    root: Optional[str]


@attr.s
class TaskDesign:
    title: str = attr.ib()
    root: str = attr.ib()
    terminal_designs: Iterable[TerminalDesignType] = attr.ib()
