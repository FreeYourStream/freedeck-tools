#!/bin/bash
INPUT="page_list.txt"
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

NAME_LIST=()
PAGE_LIST=()

while IFS="," read -r process_name page_index; do
    
    NAME_LIST+=($process_name)
    PAGE_LIST+=($page_index)
done < $INPUT

LAST_PROCESS_NAME=""

while true; do

  PROCESS_NAME="$(cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm)"
  if [ "$PROCESS_NAME" != "$LAST_PROCESS_NAME" ]; then
    echo "$PROCESS_NAME"
    LAST_PROCESS_NAME=$PROCESS_NAME
    for i in ${!NAME_LIST[*]}; do
      NAME="${NAME_LIST[i]}"
      PAGE="${PAGE_LIST[i]}"
      if [ "$NAME" = "$PROCESS_NAME" ]; then
        echo "3" > /dev/ttyACM0
        echo "$PAGE" > /dev/ttyACM0
      fi
    done
  fi;
  sleep 0.01;
done;