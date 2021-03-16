
import psutil
import serial
import time
import threading, win32gui, win32process, psutil
from win32gui import GetWindowText, GetForegroundWindow

# Everything for the serial connection
freedeckPort = "COM12" # or /dev/ttyACM0
freedeck = serial.Serial(freedeckPort, '4000000') # Create the freedeck communication port

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
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow()) #This produces a list of PIDs active window relates to
    processName = psutil.Process(pid[-1]).name()
    processName = processName.split(".exe")[0]

    if processName != processNameLast:  # If its not the same as last
        processNameLast = processName   # Make it the last so we dont check again
        print("New process: ", processName)
        for process in processList:
            processLine = process.split(",")
            if processLine[0] == processName:
                freedeck.write(str.encode("3"))
                freedeck.write(str.encode(processLine[1].strip(" ")[0]))

                print("Found process: ", processLine[0], "so send ", processLine[1], "to the freedeck")

    time.sleep(0.1)