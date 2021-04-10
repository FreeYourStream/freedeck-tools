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
PAGE_START_LIST=()
PAGE_END_LIST=()

while IFS="," read -r process_name page_start page_end; do
    NAME_LIST+=($process_name)
    PAGE_START_LIST+=($page_start)
    echo $page_end
    PAGE_END_LIST+=(${page_end:=0})

done < $INPUT
echo "asd" ${PAGE_END_LIST[@]}
LAST_PROCESS_NAME=""

DEVICE=$(cat .device_path)

changePage() {
  # echo $PAGE
  START="${1//[$'\t\r\n ']}"
  END="${2//[$'\t\r\n ']}"
  TARGET="${3//[$'\t\r\n ']}"
  echo $START $END $TARGET
  if [[ "$TARGET" -gt "$END" ]] || [[ "$TARGET" -lt "$START" ]]; then
    echo -ne "\x3\n\x31\n$1\n" > "$DEVICE"
  fi;
}

while true; do

  PROCESS_PATH="$(cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/cmdline | tr '\0' ' ')"
  PROCESS_COMMAND=${PROCESS_PATH##*/}
  PROCESS_NAME=$(echo "$PROCESS_COMMAND" | awk '{print $1}')
  if [ "$PROCESS_NAME" != "$LAST_PROCESS_NAME" ]; then
    echo $PROCESS_NAME
    LAST_PROCESS_NAME=$PROCESS_NAME
    for i in ${!NAME_LIST[*]}; do
      NAME="${NAME_LIST[i]}"
      PAGE_START="${PAGE_START_LIST[i]}"
      PAGE_END="${PAGE_END_LIST[i]}"
      if [ "$NAME" = "$PROCESS_NAME" ]; then
        (read RESULT < "$DEVICE"; changePage $PAGE_START $PAGE_END $RESULT)&
        echo -ne "\x3\n\x30\n" > "$DEVICE"
      fi
    done
  fi;
  sleep 0.05;
done;
