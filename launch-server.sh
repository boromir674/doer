#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal SERVER

cd ${git_root[$choice]}

python3 run-server.py
