from abc import ABC, abstractclassmethod


class ScriptGeneratorInterface(ABC):
    
    @abstractclassmethod
    def generate(self, *args, **kwargs):
        """Generate a script file and save on disk."""
        raise NotImplementedError
