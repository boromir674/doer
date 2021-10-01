PYDOER - CLI Application
=====================================

PyDoer is a CLI application aiming to automate executing multiple commands in different
terminal consoles.


Featuring

- Terminal Configuration as code
- Design Menu and commands using json config
- Launch/Close commands


========
Overview
========

* Free software: GNU General Public License v3.0

Prerequisites
=============

You need to have Python, Bash and gnome-terminal installed.

Installation
============


To install the PyDoer:

1. Get the code

    git clone git@github.com/boromir674/pydoer.git

2. Navigate in the 'python-doer' directory in the project's root folder
3. Install python 'pydoer' package and cli command by running (better inside a virtual env; ie using virtualenv):

From a virtual environment:

::

    pip install .

or else you could install in the "user space" with

    python3 -m pip install --user .

4a. Define useful aliases

    Assuming you cloned the code in directory '/data/repos/doer'

    alias doer='/data/repos/doer/env/bin/pydoer menu /data/tools/doer/python-doer/menu_entries.json'
    alias close-doing='/data/repos/doer/env/bin/pydoer close-doing'

4b. Define usuful symbolic link

    sudo ls -s /data/repos/doer/env/bin/pydoer /usr/local/bin/pydoer

Usage
=====

To run, simply execute (either from within the virtual env or if you installed with user/global scope):

    pydoer

The program parses the entries defined in json format in the '/data/tools/doer/python-doer/menu_entries.json' file and renders
an interactive "Menu" in the terminal, waiting for the user to make a selection.
Each selection, generates certain bash scripts stored in '/data/tools/doer/python-doer/generated_bash_scripts', which hold commands according to the parsed
json contents and spawns various terminal applications (which run the scripts' commands) to facilitate the user's activities.
