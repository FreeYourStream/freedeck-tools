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
            "bash", "-c", "cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/cmdline | tr '\\0' ' '"]
        import subprocess
        process = subprocess.Popen(bashCMD, stdout=subprocess.PIPE)
        processPath, error = process.communicate()
        processName = processPath.decode('utf-8').split("/")[-1].split(" ")[0]
    return processName


freedeck = FreeDeckSerialAPI(port="/dev/ttyACM0")

pageListFile = open("page_list.txt", "r")

# Create the page list
page_list = []
for row in map(lambda row: row.rstrip("\r\n"), pageListFile.readlines()):
    cols = row.split(",")

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
        for name, start, end in page_list:
            if name != processName:
                continue
            if end != None:
                currentPage = freedeck.getCurrentPage()
                print("CURRENTPAGE", currentPage)
                if start <= currentPage and end >= currentPage:
                    break

            print(freedeck.setCurrentPage(start))
            print("=>", name, "=", start, "=> freedeck")

    time.sleep(0.02)