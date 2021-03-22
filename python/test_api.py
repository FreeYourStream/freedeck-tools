#!/bin/python3
from lib.api import FreeDeckSerialAPI
import time
api = FreeDeckSerialAPI()

time.sleep(1)

print(api.getPageCount())
