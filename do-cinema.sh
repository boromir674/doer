#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
my_dir_mod=$(echo $my_dir | sed -e 's/\//\\\//g')

### Comment in or out commands to be executed in MPETA shell ###
cmds[1]=$my_dir_mod"\/launch-movies.py"

# delete between two patterns, exclusive
sed -i".bak" '/## COMMANDS ##/,/####/{//!d}' $my_dir/launch-mpeta.sh

# inject commands as code in shell script
for i in "${cmds[@]}"; do
    sed -i".bak" "s/\(## COMMANDS ##\)/\1\\n$i/g" $my_dir/launch-mpeta.sh
done

gnome-terminal -e "bash --rcfile $my_dir/launch-mpeta.sh"
wmctrl -r Terminal -N CINEMA
