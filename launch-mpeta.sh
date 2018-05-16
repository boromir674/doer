#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal MPETA

cd ${proj_root[$choice]}

## Do NOT modify the following section. It is managed by menu.sh, which injects code dynamically here.

## COMMANDS ##
emacs $DATA/thesis/code/pipeline.cfg >/dev/null 2>&1 &
texmaker $DATA/thesis/report/intro/introduction.tex >/dev/null 2>&1 &
####
