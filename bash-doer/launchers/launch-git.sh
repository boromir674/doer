#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

prepare-terminal GIT

cd ${git_root[$choice]}

git log --graph --all --oneline  --decorate | head -n25
git status
