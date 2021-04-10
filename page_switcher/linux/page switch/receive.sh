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

DEVICE=$(cat .device_path)

example() {
  echo $1
}

(read RESULT < "$DEVICE"; example $RESULT)&
echo -ne "\x3\n\x10\n" > "$DEVICE"
