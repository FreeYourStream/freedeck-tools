from typing import Iterable
from .utils import getFreeDeckPort
import serial

# you should wait (number of displays * 30ms) after a page changing command
# if you want to immediately call the api again to give the freedeck time
# to finish refreshing

commands = {
    "init": 0x3,
    "getFirmwareVersion": 0x10,
    "getCurrentPage": 0x30,
    "setCurrentPage": 0x31,
    "getPageCount": 0x32
}


class FreeDeckSerialAPI:
    freedeck: serial.Serial = None
    pageCount: int

    def __init__(self, port: str = None):
        if port != None:
            self.freedeck = serial.Serial(port, 4000000)
        else:
            self.freedeck = serial.Serial(getFreeDeckPort(), 4000000)
        self.pageCount = self.getPageCount()

    def intToAsciiVal(self, number: int):
        numberStr = str(number)
        numberCharArr = []
        for char in numberStr:
            numberCharArr.append(ord(char))
        return numberCharArr

    def prepare(self, data: Iterable):
        dataWithNL = bytearray()
        for bytes in data:
            if isinstance(bytes, list):
                for byte in bytes:
                    dataWithNL.append(byte)
            else:
                dataWithNL.append(bytes)
            dataWithNL.append(0xa)
        return dataWithNL

    def writeOnly(self, data: Iterable):
        self.freedeck.read_all()
        self.freedeck.write(self.prepare(data))
        return

    def readWrite(self, data: Iterable):
        self.freedeck.read_all()
        self.freedeck.write(self.prepare(data))
        return self.freedeck.read_until().decode('utf-8').rstrip("\r\n")

    def getFirmwareVersion(self):
        return self.readWrite([commands['init'], commands["getFirmwareVersion"]])

    def getCurrentPage(self):
        return int(self.readWrite([commands['init'], commands["getCurrentPage"]]))

    def setCurrentPage(self, page: int):
        if page > self.pageCount - 1:
            print("OOB")
            return
        return self.readWrite(
            [commands['init'], commands["setCurrentPage"], self.intToAsciiVal(page)])

    def getPageCount(self):
        return int(self.readWrite([commands['init'], commands['getPageCount']]))
