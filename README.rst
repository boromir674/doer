PYDOER - CLI Application
=====================================

PyDoer is a CLI application aiming to automate executing multiple command in different
terminal consoles.


Featuring

- blah blah
- kai blah blah


========
Overview
========

* Free software: GNU General Public License v3.0

Prerequisites
=============

You need to have Python, Perl and Bash installed.

Installation
============


To install the PyDoer:

1. Get the code
2. Navigate in the the 'python-doer' directory in the project's root folder
3. Install python 'pydoer' package and cli command by running (better inside a virtual env; ie using virtualenv):

::

    pip install pydoer

4. Define recommended aliases

Assuming you cloned the code in directory '/data/repos/doer'

    alias doer='pydoer /data/tools/doer/python-doer/generated_bash_scripts /data/tools/doer/python-doer/menu_entries.json'
    alias close-doing='perl /data/tools/doer/close-doing.pm'


Usage
=====

To run, simply execute::

    pydoer

The program parses the entries defined in json format in the '/data/tools/doer/python-doer/menu_entries.json' file and renders
an interactive "Menu" in the terminal, waiting for the user to make a selection.
Each selection, generates certain bash scripts stored in '/data/tools/doer/python-doer/generated_bash_scripts', which hold commands according to the parsed
json contents and spawns various terminal applications (which run the scripts' commands) to facilitate the user's activities.
