#!/bin/python3

from lib.utils import getWindowProcessName
from lib.api import FreeDeckSerialAPI
import time


freedeck = FreeDeckSerialAPI()


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
                if start <= currentPage and end >= currentPage:
                    break

            freedeck.setCurrentPage(start)
            print("=>", name, "=", start, "=> freedeck")

    time.sleep(0.02)
