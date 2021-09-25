#!/bin/bash

my_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $my_dir/definitions.sh

cmds[5]="source \$DATA\/thesis\/scripts\/add-aliases.sh"
cmds[4]="emacs \$DATA\/thesis\/code\/train.cfg >\/dev\/null 2>\&1 \&"
cmds[3]="emacs \$DATA\/thesis\/code\/pipeline.cfg >\/dev\/null 2>\&1 \&"
cmds[2]="emacs \$DATA\/thesis\/code\/regularizers.cfg >\/dev\/null 2>\&1 \&"
cmds[1]="texmaker \$DATA\/thesis\/report\/main.tex >\/dev\/null 2>\&1 \&"

# delete between two patterns, exclusive
sed -i".bak" '/## COMMANDS ##/,/####/{//!d}' $my_dir/launch-mpeta.sh

# inject commands as code in mpeta script between the ## COMMANDS ## and #### found
for i in "${cmds[@]}"; do
    sed -i".bak" "s/\(## COMMANDS ##\)/\1\\n$i/g" $my_dir/launch-mpeta.sh
done

gnome-terminal -e "bash --rcfile $my_dir/launch-git.sh"
gnome-terminal -e "bash --rcfile $my_dir/launch-mpeta.sh"
gnome-terminal -e "bash --rcfile $my_dir/launch-ipython2.sh"
wmctrl -r Terminal -N IPYTHON
