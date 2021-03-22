#!/bin/python3
import lib.api
import time
api = lib.api.FreeDeckSerialAPI()

while True:
    print(api.getCurrentPage())
    time.sleep(0.1)
