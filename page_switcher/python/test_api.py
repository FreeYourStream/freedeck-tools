#!/bin/python3
from lib.api import FreeDeckSerialAPI
import time
api = FreeDeckSerialAPI()

print("FreeDeck Serial Test")
print("--------------------")
print("Firmware: %s" % api.getFirmwareVersion())
print("Page Count: %i" % api.getPageCount())
print("Current Page: %i" % api.getCurrentPage())
