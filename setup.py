import os
import re
from collections import OrderedDict

from setuptools import setup

my_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
PRODUCTION_CODE_SOURCE = 'src'
PYPI_PACKAGE_NAME = 'pydoer'
SOURCE_CODE_REPO_SITE = 'https://github.com/boromir674/doer'
CHANGELOG = '{}/blob/master/CHANGELOG.rst'.format(SOURCE_CODE_REPO_SITE)


with open(os.path.join(my_dir, PRODUCTION_CODE_SOURCE, PYPI_PACKAGE_NAME, '__init__.py')) as f:
    _version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


setup(
    name=PYPI_PACKAGE_NAME,
    version=_version,

    author_email='boromir674@hotmail.com',

    project_urls=OrderedDict([
        ("Issue Tracker", f'{SOURCE_CODE_REPO_SITE}/issues'),
        ("Changelog", CHANGELOG),
        ("Source", SOURCE_CODE_REPO_SITE),
        # ("Documentation", "https://pydoer.readthedocs.io/en/v{}/".format(_version)),
    ]),

    entry_points={
        'console_scripts': [
            'pydoer = pydoer.menu_creator:cli',
        ]
    },

    # Folder where modules, with unit-test code, reside. Specifying this argument enables use of the test command
    # to run the specified test suite, e.g. via setup.py test.
    test_suite='tests',

    # help easy_install (a cli provided by setuptools) do its tricks
    download_url='https://github.com/boromir674/doer/archive/v{}.tar.gz'.format(_version),
)
