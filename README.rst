PYDOER - CLI Application
=====================================

PyDoer is a CLI application aiming to automate executing multiple commands in different
terminal applications.



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


Install PyDoer in virtual environment:

1. Get the code

    git clone git@github.com:boromir674/doer.git

2. Install in a python virtual environment

    cd doer

    virtualenv env --python=python3
    source env/bin/activate

    pip install python-doer


3. Make pydoer cli available in path
    Assuming ~/.local/bin is in $PATH


::

    ln -s $PWD/env/bin/pydoer ~/.local/bin/pydoer


4. (Optional) Define useful aliases

Assuming you cloned the code in directory '/data/repos/doer'

::

    alias doer='/data/repos/doer/env/bin/pydoer menu /data/repos/doer/python-doer/menu_entries.json'
    alias close-doing='/data/repos/doer/env/bin/pydoer close-doing'


Install PyDoer for user:

1. Get the code

    git clone git@github.com:boromir674/doer.git

2. Install for user

    cd doer

    pip install --user python-doer

The pydoer cli should now be (automatically) in $PATH

3. (Optional) Define useful aliases

::

    alias doer='pydoer menu /data/repos/doer/python-doer/menu_entries.json'
    alias close-doing='pydoer close-doing'


Usage
=====

To run, simply execute (either from within the virtual env or if you installed with user/global scope):

    pydoer

Basically you have 2 commands:
    1. show interactive menu

        ::

            pydoer menu </path/to/menu.json>

        The program parses the entries defined in json formatted file defined by the user json' file and renders
        an interactive "Menu" in the terminal, waiting for the user to make a selection.
        Each selection, generates a 'do' script which is responsible for opening/spawning one or more terminal applications.
        For each terminal application, a 'launch' script is generated which is responsible for running certain commands on that terminal.

    2. close windows spawned from previous activity

        ::

            pydoer close-doing
