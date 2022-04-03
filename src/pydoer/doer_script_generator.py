import os

import attr

from pydoer.script_generator import ScriptGeneratorInterface


class FileScriptGenerator(ScriptGeneratorInterface):

    def generate(self, *args, **kwargs):
        content: str = args[0]
        file_path: str = args[1]
        with open(file_path, 'w') as _file:
            _file.write(content)
        return file_path


@attr.s
class DoerScriptGenerator:
    output_dir: str = attr.ib()
    script_generator: ScriptGeneratorInterface = attr.ib(default=attr.Factory(FileScriptGenerator))

    def generate(self, contents: str, name: str):
        return self.script_generator.generate(contents, os.path.join(self.output_dir, name))
