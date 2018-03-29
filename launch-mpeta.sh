#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal MPETA

cd ${git_root[$choice]}

## Do NOT modify the following section. It is managed by menu.sh, which injects code dynamically here.

## COMMANDS ##
emacs $PROJECTS/knowfly/green-machine/green-web/app.py &
####
