"""Module for representing/reading the user design of a terminal."""

from typing import Dict, Iterable, Protocol, Union, Optional
import attr
import json


@attr.s
class WindowDesign:
    title: str = attr.ib(default=None)


class WindowDesignType(Protocol):
    title: str


@attr.s
class TerminalDesign:
    commands: Iterable[str] = attr.ib(default=[])
    root: Union[str, None] = attr.ib(default=None)
    window_title: Union[str, None] = attr.ib(default=None)

    @classmethod
    def from_json(cls, data: str):
        data_dict = json.loads(data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_dict(cls, data: dict):
        return TerminalDesign(
            data.get('commands', []),
            data.get('root'),
            data.get('title'),
        )
