#!/bin/python3
import os


def getWindowProcessName():
    if os.name == 'nt':
        import win32gui
        import win32process
        # This produces a list of PIDs active window relates to
        pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
        processName = psutil.Process(pid[-1]).name()
        processName = processName.split(".exe")[0]
    else:
        bashCMD = [
            "bash", "-c", "cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/cmdline | tr '\\0' ' '"]
        import subprocess
        process = subprocess.Popen(bashCMD, stdout=subprocess.PIPE)
        processPath, error = process.communicate()
        processName = processPath.decode('utf-8').split("/")[-1].split(" ")[0]
    return processName


def execBash(command):
    import subprocess
    response, error = subprocess.Popen(
        ["bash", "-c", command], stdout=subprocess.PIPE).communicate()
    return response


def binaryToString(binary):
    return binary.decode("utf-8").rstrip("\r\n")


def findFreeDeckDeviceWin():
    return "COM14"  # automate this


def findFreeDeckDeviceLinux():
    import subprocess
    devices = execBash("find /sys/bus/usb/devices/usb*/ -name dev")

    for device in devices.splitlines():
        devicePath = device.decode("utf-8").rstrip("/dev")
        deviceNameRaw = execBash("udevadm info -q name -p %s" % devicePath)
        deviceName = binaryToString(deviceNameRaw)
        if deviceName.find("bus/") != -1:
            continue

        info = execBash(
            "eval $(udevadm info -q property --export -p %s) && echo $ID_VENDOR_ID:$ID_MODEL_ID:$SUBSYSTEM" % devicePath)
        identifier = binaryToString(info)
        if identifier == "2341:8037:tty":
            return "/dev/%s" % deviceName
    return "/dev/ttyACM0"


def getFreeDeckPort():
    if os.name == "nt":
        return findFreeDeckDeviceWin()
    else:
        return findFreeDeckDeviceLinux()


# if __name__ == "__main__":
#     print(getFreeDeckPort())
