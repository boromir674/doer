"""Module for reading a design of a Menu (static assets & items)."""

import json
import os
from typing import Iterable, Protocol

import attr


class ItemTask(Protocol):
    root: str
    terminal_designs: Iterable


class TerminalDesign(Protocol):
    root: str


@attr.s
class MenuConfig:
    title: str = attr.ib()
    subtitle: str = attr.ib()
    item_tasks: Iterable[ItemTask] = attr.ib()

    @property
    def options(self):
        return self.item_tasks

    def __attrs_post_init__(self):
        for task in self.item_tasks:
            for terminal in task.terminal_designs:
                if task.root:  # indication for using a master task root dir
                    if not terminal.root:
                        # make terminal root same as master root dir
                        terminal.root = task.root
                    elif not terminal.root.startswith('/'):
                        # if terminal root dir is a relative path
                        # make relative path absolute using master task root
                        terminal.root = os.path.join(task.root, terminal.root)

    @classmethod
    def from_dict(cls, data: dict):
        return MenuConfig(
            data.get('title', 'DOER'),
            data.get('subtitle', 'DO IT, DO IT NOW!'),
            data.get('tasks', [])
        )

    @classmethod
    def from_json_file(cls, json_file: str):
        with open(json_file, 'r') as j_file:
            data_dict = json.loads(j_file.read())
        return cls.from_dict(data_dict)
