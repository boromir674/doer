import json

from pydoer.task_design import TaskDesign
from pydoer.terminal_design import TerminalDesign

__all__ = ['TaskDesignFactory']


class TaskDesignFactory:

    @classmethod
    def from_json_file(cls, file_path: str):
        with open(file_path, 'r') as terminal_design_file:
            design = terminal_design_file.read()
            return cls.from_json(design)

    @classmethod
    def from_json(cls, json_string: str):
        data_dict = json.loads(json_string)
        return cls.from_dict(data_dict)

    @classmethod
    def from_dict(cls, data: dict):
        return TaskDesign(
            # data['_id'],
            data['name'],
            data.get('root'),
            [TerminalDesign.from_dict(x) for x in data.get('terminals')]
        )
