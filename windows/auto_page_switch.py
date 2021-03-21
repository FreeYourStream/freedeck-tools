#!/bin/python3

import psutil
import serial
import time
import psutil
import os

# Everything for the serial connection
if os.name == 'nt':
    freedeckPort = "COM12"  # or /dev/ttyACM0
else:
    freedeckPort = "/dev/ttyACM4"
# Create the freedeck communication port
freedeck = serial.Serial(freedeckPort, '4000000')

# Create the process list
processList = []
page_list = open("page_list.txt", "r")

for program in page_list:
    processList.append(program.rstrip("\n").rstrip("\r").rstrip(" "))

# Some variable to track things
processName = ""
processNameLast = "-"

# The while loop
while(1):
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

    if processName != processNameLast:  # If its not the same as last
        processNameLast = processName   # Make it the last so we dont check again
        print("New process: ", processName)
        for process in processList:
            processLine = process.split(",")
            if processLine[0] == processName:
                packet = bytearray()
                packet.append(0x3)
                packet.append(0xa)
                packet.append(0x31)
                packet.append(0xa)
                packet.append(ord(processLine[1].strip(" ")[0]))
                packet.append(0xa)
                freedeck.write(packet)

                print("Found process: ",
                      processLine[0], "so send ", processLine[1], "to the freedeck")

    time.sleep(0.1)
