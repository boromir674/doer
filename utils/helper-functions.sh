set-title () {
  if [[ -z "$ORIG" ]]; then
    ORIG=$PS1
  fi
  TITLE="\[\e]2;$*\a\]"
  PS1=${ORIG}${TITLE}
}

prepare-terminal () {
    # arg1: the desired terminal title
    source $my_dir/doerrc
    $(echo $titlesetter) $1 >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Did not find a sourced '$titlesetter' function"
    fi
}
