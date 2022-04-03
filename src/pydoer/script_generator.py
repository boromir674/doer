from abc import ABC, abstractmethod


class ScriptGeneratorInterface(ABC):

    @abstractmethod
    def generate(self, *args, **kwargs):
        """Generate a script file and save on disk."""
        raise NotImplementedError
