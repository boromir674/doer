#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
my_dir_mod=$(echo $my_dir | sed -e 's/\//\\\//g')

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

#cmds[2]="rstudio >\/dev\/null 2>\&1 \&"
# cmds[2]="emacs \$DATA\/thesis\/code\/pipeline.cfg >\/dev\/null 2>\&1 \&"
cmds[1]="xdg-open \$PROJECTS\/dm\/Vampire_The_Requiem_okular.pdf >\/dev\/null 2>\&1 \&"

# delete between two patterns, exclusive
sed -i".bak" '/## COMMANDS ##/,/####/{//!d}' $my_dir/launch-mpeta.sh

# inject commands as code in shell script
for i in "${cmds[@]}"; do
    sed -i".bak" "s/\(## COMMANDS ##\)/\1\\n$i/g" $my_dir/launch-mpeta.sh
done

gnome-terminal -e "bash --rcfile $my_dir/launch-git.sh"
gnome-terminal -e "bash --rcfile $my_dir/launch-mpeta.sh"
