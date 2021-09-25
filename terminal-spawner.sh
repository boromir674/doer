spawn-terminal () {}
	terminal_title=$1
	# use this argument to have a custom set of commands executed immediatley after the new terminal has been spawned
	custom_rc_file_path=$2
  	gnome-terminal -e "bash --rcfile $2"
  	wmctrl -r Terminal -N $terminal_title
}


spawn-terminal $1 $2



# while getopts u:p: option 
# do 
#  case "${option}" 
#  in 
#  u) USER=${OPTARG};; 
#  p) PASSWORD=${OPTARG};; 
#  esac 
# done 
 
# echo "User:"$USER 
# echo "Password:"$PASSWORD