import serial
import socket
import time


def send_tcp(server, data, port, buffer=1024, timeout=3.0):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((server, port))
        s.sendall(data.encode())
        s.settimeout(timeout)
        response = s.recv(buffer)

    return response


def send_udp(bind_addr, server, data, port, buffer=1024, timeout=3.0):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        responses = []
        s.bind((bind_addr, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(data, (server, port))
        try:
            while True:
                s.settimeout(3.0)
                responses.append(s.recvfrom(buffer))
        except socket.timeout:
            return responses

def send_serial(comPort, data, baudRate, parity, stopBit, byteSize, wait):

    ser = serial.Serial(
        port=comPort,
        baudrate=baudRate,
        parity=serial.PARITY_SPACE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS
    )

    ser.isOpen()
    ser.write(data)
    time.sleep(wait)


    out = b''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    
    return out.decode()
