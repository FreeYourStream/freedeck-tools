#!/bin/python3

from typing import get_args
from fdserial.api import FreeDeckSerialAPI
import time
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
            "bash", "-c", "xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME 2>/dev/null | awk -F= '{print($2)}' "]  # "cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/cmdline | tr '\\0' ' '"]
        import subprocess
        process = subprocess.Popen(bashCMD, stdout=subprocess.PIPE)
        windowName, error = process.communicate()
        processName = windowName.decode('utf-8').strip("\n\" ")
        if processName == "":
            return "unknown"
    return processName


freedeck = FreeDeckSerialAPI(port="/dev/ttyACM0")
pageListFile = open("page_list.txt", "r")

# Create the page list
page_list = []
default_index = -1
for row in map(lambda row: row.rstrip("\r\n"), pageListFile.readlines()):
    if row[0] == "#":
        continue

    cols = row.split("#")[0].split(",")

    if cols[0] == 'DEFAULT':
        default_index = int(cols[1])
        continue

    row = []
    row.append(cols[0])  # name
    row.append(int(cols[1]))  # start

    if(len(cols) > 2):
        row.append(int(cols[2]))  # end
    else:
        row.append(None)  # end not used

    page_list.append(row)

# Some variable to track things
processNameLast = "-"

# The while loop
while(1):
    processName = getWindowProcessName()
    if processName != processNameLast:  # If its not the same as last
        processNameLast = processName   # Make it the last so we dont check again
        print("Active window:", processName)
        for index, (name, start, end) in enumerate(page_list):
            if name.lower() not in processName.lower():
                if(index == len(page_list) - 1 and default_index != -1):
                    freedeck.setCurrentPage(default_index)
                continue
            if end != None:
                currentPage = freedeck.getCurrentPage()
                if start <= currentPage and end >= currentPage:
                    break
            freedeck.setCurrentPage(start)
            print("Matched =>", name, "= Page", start)
            break

    time.sleep(0.02)
