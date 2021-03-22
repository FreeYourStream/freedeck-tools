from typing import Iterable
from lib.utils import getFreeDeckPort
import serial

commands = {
    "init": 0x3,
    "getCurrentPage": 0x30,
    "setCurrentPage": 0x31
}


class FreeDeckSerialAPI:
    freedeck: serial.Serial = None

    def __init__(self):
        self.freedeck = serial.Serial(getFreeDeckPort(), 4000000)

    def intToAsciiVal(self, number: int):
        return ord(str(number))

    def prepare(self, data: Iterable):
        dataWithNL = bytearray()
        for byte in data:
            dataWithNL.append(byte)
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

    def getCurrentPage(self):
        return int(self.readWrite([commands['init'], commands["getCurrentPage"]]))

    def setCurrentPage(self, page: int):
        return self.writeOnly([commands['init'], commands["setCurrentPage"], self.intToAsciiVal(page)])
