from modules.modules import ThreadModule
from tools import Tools
import netifaces as ni
import array
import fcntl
import socket
import struct


class Network(ThreadModule):
    """
    Network Module
    Shows the current IP address and status of the given interface
    For WiFi interfaces, shows the assigned access point's ESSID
    """

    MAX_LENGTH_INTERFACE = 16
    MAX_LENGTH_ESSID = 32
    SIOCGIWESSID = 0x8B1B

    defaults = {
        "icon": Tools.sym(""),
        "icon_wifi": Tools.sym("")
    }

    def __init__(self, interface=None, interval=5, template=None, **kwargs):
        if template:
            super().__init__(template, interval, **kwargs)
        else:
            super().__init__("$icon $ip", interval, **kwargs)
        if interface:
            self.interface = interface
        else:
            self.interface = "eno1"
        self.is_wifi = False
        if self.interface.startswith("wl"):
            self.is_wifi = True
        if "wifi" in kwargs:
            self.is_wifi = kwargs["wifi"]
        if self.is_wifi:
            self.values["icon"] = self.values["icon_wifi"]
        self.wifi_counter = 0

    def repeat(self):
        try:
            address = ni.ifaddresses(self.interface)
            if ni.AF_INET in address:
                self.values["ip"] = address[2][0]["addr"]
                if self.is_wifi:
                    if self.wifi_counter >= 1:
                        ssid = self.get_essid()
                        self.values["essid"] = ssid if ssid else ""
                        self.wifi_counter = 0
                    self.wifi_counter += 1
                else:
                    self.values["essid"] = ""
            else:
                self.values["ip"] = "down"
                self.values["essid"] = ""
        except ValueError:
            self.values["ip"] = "ERR"

    def get_essid(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        essid = array.array("b")
        request = array.array("b")
        essid.frombytes(('\0' * Network.MAX_LENGTH_ESSID).encode())
        essid_pointer, essid_length = essid.buffer_info()

        request.frombytes(
            (self.interface.ljust(Network.MAX_LENGTH_INTERFACE, "\0")).encode() + struct.pack("PHH", essid_pointer,
                                                                                      essid_length, 0))
        fcntl.ioctl(sock.fileno(), Network.SIOCGIWESSID, request)
        name = essid.tostring().decode().rstrip('\x00')
        if name:
            return name
        return None
