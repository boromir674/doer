PYDOER - CLI Application
=====================================

PyDoer is a CLI application aiming to automate executing multiple commands in different
terminal applications.

.. start-badges

| |circleci| |codecov|
| |release_version| |wheel| |supported_versions| |commits_since|
| |better_code_hub| |sc1|

|
| **Source Code:** https://github.com/boromir674/doer
|


.. |release_version| image:: https://img.shields.io/pypi/v/pydoer
    :alt: Production Version
    :target: https://pypi.org/project/pydoer/

.. |wheel| image:: https://img.shields.io/pypi/wheel/pydoer.svg
    :alt: Python Wheel
    :target: https://pypi.org/project/pydoer

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/pydoer.svg
    :alt: Supported Python versions
    :target: https://pypi.org/project/pydoer

.. |commits_since| image:: https://img.shields.io/github/commits-since/boromir674/doer/v1.0.2/dev?logo=github
    :alt: GitHub commits on branch, since tagged version
    :target: https://github.com/boromir674/doer/compare/v1.0.2..dev



.. |circleci| image:: https://circleci.com/gh/boromir674/doer/tree/dev.svg?style=shield
    :alt: CircleCI
    :target: https://circleci.com/gh/boromir674/doer/tree/dev

.. |codecov| image:: https://img.shields.io/codecov/c/github/boromir674/doer/dev?logo=codecov
    :alt: Codecov
    :target: https://codecov.io/gh/boromir674/doer


.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/doer?branch=dev
    :alt: Better Code Hub
    :target: https://bettercodehub.com/


.. |sc1| image:: https://img.shields.io/scrutinizer/quality/g/boromir674/doer/dev?logo=scrutinizer&style=flat
    :alt: Scrutinizer code quality
    :target: https://scrutinizer-ci.com/g/boromir674/doer/?branch=dev



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

Using `pip` is the approved way for installing `pydoer`.

The command `pip install pydoer` isntalls the `pydoer` python package
and adds the cli script in your PATH.

Following the below instructions, should place the pydoer cli executable
in your PATH, assuming that you ensure the ~/.local/bin is in your PATH, if need be.

1. Install PyDoer:

   a. Install in a virtual environment (recommended)
   
       export PYTHON_VIRTUAL_ENVS_DIR=~python-envs
       export PYDOER_ENV=$PYTHON_VIRTUAL_ENVS_DIR/pydoer-env

       mkdir $PYTHON_VIRTUAL_ENVS_DIR
       cd $PYTHON_VIRTUAL_ENVS_DIR

       virtualenv $PYDOER_ENV --python=python3
       source $PYDOER_ENV/bin/activate

       pip install pydoer

       deactivate

       # make a link to the current user's local bin dir
       ln -s $PYDOER_ENV/bin/pydoer ~/.local/bin/pydoer
   
   Now the pydoer cli should be in ~/local/bin
   Simply make sure ~/local/bin is in your PATH to easily invoke the cli.

   b. Install for current user
       
       pip install --user pydoer

   Now the pydoer cli should be in ~/local/bin
   Simply make sure ~/local/bin is in your PATH to easily invoke the cli.

   c. Install (globally) for all users

       sudo pip install pydoer
   
   Now the pydoer cli should already be in your PATH.

2. Check that cli is available

       pydoer --help


Usage
=====

Firstly, you should `design` your own menu and the tasks you would like to
automate. Then you should be able to 'feed' your design into `pydoer`,
which will parse it and render the interactive menu in your terminal.

The `design` comprises of a `menu.json` file along side with an `options`
folder. In the `options` folder eash menu task is represented by a dedicated file.

See `tests/data/correct_menu_design` for an example of a menu design
to get started.

Once, finished place both the `menu.json` files and the `optinos` directory
in the same folder.

1. (Optional) Define useful aliases

Assuming you placed the `design` in the `my_doer_menu` folder:

::
    export MY_DOER_MENU=my_doer_menu


Assuming that `pydoer` is in your PATH (see Installation above)
you can define useful aliases as follows:

::

    alias doer='pydoer menu $MY_DOER_MENU'
    alias close-doing='/data/repos/doer/env/bin/pydoer close-doing'


To run, simply execute:

    pydoer


How it works
============

Basically you have 2 commands:
    1. show interactive menu

        ::

            pydoer menu </path/to/menu.json>

        The program parses the entries defined in the json formatted files defined by the user and renders
        an interactive "Menu" in the terminal, waiting for the user to make a selection.
        Each selection, generates a 'do' script which is responsible for opening/spawning one or more terminal applications.
        For each terminal application, a 'launch' script is generated which is responsible for running certain commands on that terminal.

    2. close windows spawned from previous activity

        ::

            pydoer close-doing
