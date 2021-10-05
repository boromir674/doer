PYDOER - CLI Application
=====================================

PyDoer is a CLI application aiming to automate executing multiple commands in different
terminal applications.

.. start-badges

| |circleci| |codecov|
| |release_version| |wheel| |supported_versions| |commits_since|
| |better_code_hub| |codacy| |maintainability| |codeclimate_tech_debt| |sc1|

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

.. |commits_since| image:: https://img.shields.io/github/commits-since/boromir674/pydoer/v1.0.0/master?logo=github
    :alt: GitHub commits on branch, since tagged version
    :target: https://github.com/boromir674/pydoer/compare/v1.0.0..master





.. |circleci| image:: https://circleci.com/gh/boromir674/doer/tree/master.svg?style=shield
    :alt: CircleCI
    :target: https://circleci.com/gh/boromir674/doer/tree/master

.. |codecov| image:: https://img.shields.io/codecov/c/github/boromir674/doer/master?logo=codecov
    :alt: Codecov
    :target: https://codecov.io/gh/boromir674/doer


.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/doer?branch=master
    :alt: Better Code Hub
    :target: https://bettercodehub.com/

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/95d0b7816b9d4f17a986a877cc16c64a
    :alt: Codacy
    :target: https://www.codacy.com/gh/boromir674/doer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=boromir674/doer&amp;utm_campaign=Badge_Grade

.. |maintainability| image:: https://api.codeclimate.com/v1/badges/b5bdd6ec9c1dad2fe2d0/maintainability
    :alt: Maintainability
    :target: https://codeclimate.com/github/boromir674/doer/maintainability

.. |codeclimate_tech_debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/doer?logo=code%20climate
    :alt: Code Climate technical debt
    :target: https://codeclimate.com/github/boromir674/doer/trends/technical_debt

.. |sc1| image:: https://img.shields.io/scrutinizer/quality/g/boromir674/doer/master?logo=scrutinizer&style=flat
    :alt: Scrutinizer code quality
    :target: https://scrutinizer-ci.com/g/boromir674/doer/?branch=master



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
