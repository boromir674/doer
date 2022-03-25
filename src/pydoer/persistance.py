import os
import attr


my_dir = os.path.dirname(os.path.realpath(__file__))
PERSIST_FILE_NAME = '.windows_opened_by_doer.txt'


@attr.s
class PersistanceManager:
    cache_file: str = attr.ib(
        # improve: replace default path value with current working dir
        default=os.path.join(my_dir, PERSIST_FILE_NAME))

    def save(self, string):
        with open(self.cache_file, 'a') as file_:
            file_.write(string + '\n')

    def read(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file_:
                return file_.read()
        else:
            return ''

    def iter_windows(self):
        windows_string = self.read()
        for line in windows_string.split('\n'):
            if line:
                yield line
            elif line == '':
                continue
            else:
                raise RuntimeError(f"Wierd formmated line: {line}")

    def flush(self):
        """Remove windows 'remembered' in the cache file."""
        with open(self.cache_file, 'w') as _:
            pass
