import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup

my_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
src = 'src'
name = 'pydoer'
source_code_repo = 'https://github.com/boromir674/doer'
changelog = '{}/blob/master/CHANGELOG.rst'.format(source_code_repo)


with open(os.path.join(my_dir, src, name, '__init__.py')) as f:
    _version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open(os.path.join(my_dir, 'requirements.txt'), 'r') as f:
    requirements = [python_package.strip() for python_package in f.readlines()]


setup(
    name=name,
    version=_version,
    long_description_content_type='text/x-rst',

    author='Konstantinos Lampridis',
    author_email='boromir674@hotmail.com',
    license='GNU GPLv3',

    install_requires=requirements,

    project_urls=OrderedDict([
        ("Issue Tracker", f'{source_code_repo}/issues'),
        ("Changelog", changelog),
        ("Source", source_code_repo),
        # ("Documentation", "https://pydoer.readthedocs.io/en/v{}/".format(_version)),
    ]),

    entry_points={
        'console_scripts': [
            'pydoer = pydoer.menu_creator:cli',
        ]
    },

    # Folder where unittest.TestCase-like written modules reside. Specifying this argument enables use of the test command
    # to run the specified test suite, e.g. via setup.py test.
    test_suite='tests',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Home Automation',
        'Topic :: Utilities'
    ],

    download_url='https://github.com/boromir674/doer/archive/v{}.tar.gz'.format(_version),  # help easy_install do its tricks



    # A string or list of strings specifying what other distributions need to be present in order for the setup script to run.
    # (Note: projects listed in setup_requires will NOT be automatically installed on the system where the setup script is being run.
    # They are simply downloaded to the ./.eggs directory if they're not locally available already. If you want them to be installed,
    # as well as being available when the setup script is run, you should add them to install_requires and setup_requires.)
    # setup_requires=[],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     'music_album_creation.format_classification': ['data/*.txt', 'data/model.pickle'],
    # },

    # A dictionary mapping names of "extras" (optional features of your project: eg imports that a console_script uses) to strings or lists of strings
    # specifying what other distributions must be installed to support those features.
    # extras_require={},
)
