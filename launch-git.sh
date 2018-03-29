#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal GIT

cd ${git_root[$choice]}

git branch
git status
git diff --stat
