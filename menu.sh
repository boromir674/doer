#!/bin/bash

my_dir=$DATA/tools/doer
. $my_dir/definitions.sh

# clear the screen
tput clear

# Move cursor to screen location X,Y (top left is 0,0)
tput cup 3 15

# Set a foreground colour using ANSI escape
tput setaf 3
echo "DO IT, DO IT NOW!"
tput sgr0

tput cup 5 17
# Set reverse video mode
tput rev
echo "M A I N - M E N U"
tput sgr0

tput cup 7 15
echo 1. ${menu[1]}

tput cup 8 15
echo 2. ${menu[2]}

tput cup 9 15
echo 3. ${menu[3]}

tput cup 10 15
echo 4. ${menu[4]}

# Set bold mode
tput bold
tput cup 12 15
read -p "Enter your choice [1-${#menu[@]}] " choice

tput clear
tput sgr0
tput rc

pref=launch

# inject choice in definitions to be read by scripts
sed -i".bak" "s/\(choice=\)\(.\+\)\?/\1$choice/" $my_dir/definitions.sh

if [[ -z ${menu[$choice]} ]]; then
    echo "Nothing selected to do"
    exit
fi

echo Chosen to do \'${menu[$choice]}\'
$my_dir/${execu[$choice]}
echo Executed script \'${execu[$choice]}\'
