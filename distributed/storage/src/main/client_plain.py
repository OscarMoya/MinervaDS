import sys
import os
import random
import socket
import subprocess

def get_client_ip_by_iface(ifname):
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_client(mgmt_ip=None,mgmt_port=9797,data_ip="10.10.100.100",data_port=9696):
    if not mgmt_ip:
        try:
            mgmt_ip = get_client_ip_by_iface("eth0")
            if not mgmt_ip:
                raise Exception
        except:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 0))
            mgmt_ip = s.getsockname()[0]
    id = "Server-" + str(random.randint(1,1000))
    client_manager = ClientManager(id=id)
    client_manager.start(mgmt_ip, mgmt_port, data_ip, data_port)
    return client_manager


path = os.path.abspath(__file__)
path = path.split("/")
path = "/".join(path[0:4])
sys.path.append(path)

#Cleaning DBs
command = "rm -rf clientfile"

try:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
except:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

from distributed.storage.src.module.client.manager import ClientManager
