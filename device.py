from asyncio.windows_events import NULL
from sre_constants import NOT_LITERAL


class Device:

    def __init__(self, serial, mac):
        self.serial = serial
        self.mac = mac

    def __init__(self):
        self.serial = NULL
        self.mac = NULL

    def __init__(self, ip):
        self.serial = NULL
        self.mac = NULL

    def setIP(self, ip):
        self.ip = ip

    