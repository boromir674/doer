#!/bin/bash

doer_root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define a 'choice => menu label' hash
declare -A menu

menu[1]=Thesis
menu[2]=Cinema
menu[3]="Green Web"
menu[4]="Green Magic"

# Define a 'choice => executable' hash
declare -A execu
pre=do

execu[1]="$pre-thesis.sh"
execu[2]="$pre-cinema.sh"
execu[3]="$pre-green-web.sh"
execu[4]="$pre-green-magic.sh"

# Define a 'choice => source control root directory' hash
declare -A git_root

git_root[1]="$DATA/thesis/code"
# git_root[2]=Cinema
git_root[3]="$PROJECTS/knowfly/green-machine/green-web"
git_root[4]="$PROJECTS/knowfly/green-machine/green-magic/"

# Define a terminal title-setter function
# This value should correspond to a function most probably defined in a file such as ~/.bash_functions
titlesetter=set-title

# choice variable is set dynamically
choice=3

function prepare-terminal {
    # arg1: the desired terminal title
    source $my_dir/doerrc
    $(echo $titlesetter) $1 >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Did not find a sourced '$titlesetter' function"
    fi
}
