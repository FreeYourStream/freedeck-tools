#!/bin/python3

# Import the required python modules
from fdserial.api import FreeDeckSerialAPI
import time
import os
import psutil

# \/ EDIT BELOW IF REQUIRED \/ #

config = {
    # File in wich the processes are saved
    "pageFile": 'page_list.txt',
    # Define which serial port to use
    "serialPort": 'com5'
}

# \/ DO NOT EDIT BELOW \/ #

"""
Import the required packages for Windows
"""
def import_win_packages():
    global win32gui
    global win32process

    # Import the required packages for Windows
    if os.name == 'nt':
        import win32gui
        import win32process
    
    return

"""
Get the Window Process Name from the window that is foccessed 
"""
def getWindowProcessName():
    # Windows
    if os.name == 'nt':        
        # This produces a list of PIDs active window relates to
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        processName = psutil.Process(pid[-1]).name()
        processName = processName.split(".exe")[0] # Strip .exe from the processName
    # Linux or some other OS
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

"""
Create a list with all the mapped programs from the page_list file.
"""
def createPageList():
    page_list = list()
    default_index = -1
    for row in map(lambda row: row.rstrip("\r\n"), pageListFile.readlines()):
        # Skip commented rows
        if row[0] == "#":
            continue

        cols = row.split("#")[0].split(",")

        if cols[0] == 'DEFAULT':
            default_index = int(cols[1])
            continue

        row = list()
        row.append(cols[0])  # name
        row.append(int(cols[1]))  # start

        if(len(cols) > 2):
            row.append(int(cols[2]))  # end
        else:
            row.append(None)  # end not used
        page_list.append(row)

    return page_list, default_index # return the values

"""
Connect to the Freedeck via a serial connection. If an Exception occurs print the Exception and stop the script
"""
# Try to connect to the FreeDeck
try:
    freedeck = FreeDeckSerialAPI(port=config['serialPort'])
except Exception as exception:
    print(exception) # print the error
    print('\033[91m[ERROR]: Cannot connect to your FreeDeck, make sure your FreeDeck is connected to your system and you have chosen the right serial port!\033[0;0m') # print a human readable error message
    exit(1) # exit the script

"""
Read the contents of the page_list file. If an Exception occurs print the Exception and stop the script
"""
try:
    pageListFile = open(config['pageFile'], "r") # Open the page_list file.
    page_list, default_index = createPageList() # List of all programs which are in the page_list file.
except Exception as exception:
    print(exception) # print the error
    print('\033[91m[ERROR]: Your page_file could not be read !\033[0;0m') # print a human readable error message
    exit(1) # exit the script

import_win_packages() # Import the required packages for Windows
processNameLast = None # Variable used to keep track which program was the last program.

"""
Run the script
"""
if __name__ == "__main__":
    while True:
        try:
            processName = getWindowProcessName()
        except:
            print('\033[91m[ERROR]: Could not find the process!\033[0;0m')

        if processName != processNameLast:  # If the program not the same as last.
            processNameLast = processName   # Set the current program as the last in the processNameLast variable so we do not change the page when this page is still open.
            print("Active window:", processName)
            for index, (name, start, end) in enumerate(page_list):
                if name.lower() not in processName.lower():
                    if(index == len(page_list) - 1 and default_index != -1):
                        freedeck.setCurrentPage(default_index) # Change the FreeDeck page
                    continue
                if end != None:
                    currentPage = freedeck.getCurrentPage() # Get the current FreeDeck page
                    if start <= currentPage and end >= currentPage:
                        break
                freedeck.setCurrentPage(start) # Change the FreeDeck page
                print("Matched:", name, "- Setting FreeDeck to page", start)
                break

        time.sleep(0.02)