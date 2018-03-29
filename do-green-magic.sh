#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

### Comment in or out commands to be executed in MPETA shell ###
cmds[2]="\\pycharm >\/dev\/null 2>\&1 \&"
cmds[1]="emacs \$PROJECTS\/knowfly\/green_machine\/green-magic\/setup.py \&"

# delete between two patterns, exclusive
sed -i".bak" '/## COMMANDS ##/,/####/{//!d}' $my_dir/launch-mpeta.sh

# inject commands as code in shell script
for i in "${cmds[@]}"; do
    sed -i".bak" "s/\(## COMMANDS ##\)/\1\\n$i/g" $my_dir/launch-mpeta.sh
done

gnome-terminal -e "bash --rcfile $my_dir/launch-git.sh"
wmctrl -r Terminal -N GIT
gnome-terminal -e "bash --rcfile $my_dir/launch-mpeta.sh"
wmctrl -r Terminal -N MPETA
gnome-terminal -e "bash --rcfile $my_dir/launch-ipython3.sh"
wmctrl -r Terminal -N IPYTHON
