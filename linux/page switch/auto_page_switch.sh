#!/bin/bash

for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && exit
        # echo "$devname"
        eval "$(udevadm info -q property --export -p $syspath)"
        [[ "$ID_VENDOR_ID:$ID_MODEL_ID:$SUBSYSTEM" != "2341:8037:tty" ]] && exit
        # echo "-----------"
        # echo "$(udevadm info -q property --export -p $syspath)"
        echo "/dev/$devname" > .device_path
    )
done

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

  PROCESS_PATH="$(cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/cmdline | tr '\0' ' ')"
  PROCESS_COMMAND=${PROCESS_PATH##*/}
  PROCESS_NAME=$(echo "$PROCESS_COMMAND" | awk '{print $1}')
  if [ "$PROCESS_NAME" != "$LAST_PROCESS_NAME" ]; then
    echo $PROCESS_NAME
    LAST_PROCESS_NAME=$PROCESS_NAME
    for i in ${!NAME_LIST[*]}; do
      NAME="${NAME_LIST[i]}"
      PAGE="${PAGE_LIST[i]}"
      if [ "$NAME" = "$PROCESS_NAME" ]; then
        DEVICE=$(cat .device_path)
        echo -n -e '\x3' > "$DEVICE"
        echo -n "$PAGE" > "$DEVICE"
        # echo "$PAGE"
      fi
    done
  fi;
  sleep 0.05;
done;
