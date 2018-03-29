#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal IPYTHON2

cd ${git_root[$choice]}

ipython
