#!/bin/sh
if [ -z "$1" ]; then
  echo "Starting up visudo with this script as first parameter"
  export EDITOR=$0 && sudo -E visudo
else
  echo "Changing sudoers"
  echo "django ALL=(ALL:ALL) ALL" >> $1
fi

# Shout outs to StackOverflow http://stackoverflow.com/a/3706774/262677

