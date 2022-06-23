import com
import socket
import re

# reference: https://github.com/StephenGenusa/Crestron-List-Devices-On-Network/blob/master/List_Crestron_Devices.py

# IP Address of this machine
cur_ip = "169.254.133.52"

# Port to send the discovery packets
port = 41794

hostname = socket.gethostname()
broadcastAddress = '255.255.255.255'
devList = [['IP', 'Hostname', 'Model', 'Version']]

# Message sent to each device for discovery
message = b"\x14\x00\x00\x00\x01\x04\x00\x03\x00\x00\x66\x65\x65\x64" + (b"\x00" * 252)


def send_command(inp):
    for i in inp:
        data, addr = i
        if addr[0] != cur_ip:
            devList.append(parse_input(data, addr))

def parse_input(data, addr):
    ipAddress = addr[0]
    hostname = re.findall(b'\x00([a-zA-Z0-9-]{2,30})\x00', data)
    ver = re.findall(b'v\d+.\d+.\d+', data)
    dev = re.findall(b'\x00([a-zA-Z0-9-]{2,30}) \[', data)
    for i in ver:
        ver = i.decode()
    for i in dev:
        dev = i.decode()
    retval = [ipAddress, hostname[0].decode(), dev, ver]
    return retval

# Finds all Crestron devices and returns a list of their IP addresses
def autodiscovery():
    send_command(com.send_udp(cur_ip, broadcastAddress, message, port))
    return [devList[i][0] for i in range(1, len(devList))]
