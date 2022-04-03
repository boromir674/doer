import os

import attr


@attr.s(frozen=True, slots=True, auto_attribs=True)
class LaunchScriptPathFinder:
    root_dir: str

    def path(self, task_name: str, subtask_name: str):
        return os.path.join(
            self.root_dir,
            'launch-' + task_name.replace(" ", "-") + '-' + subtask_name.replace(" ", "-") + '.sh')



@attr.s(frozen=True, slots=True, auto_attribs=True)
class TaskScriptPathFinder:
    root_dir: str

    def path(self, task_name: str):
        return os.path.join(
            self.root_dir,
            'do-' + task_name.replace(" ", "-") + '.sh')


