import sys
import os
import random
import subprocess
import time
import string
import commands
import threading
from distributed.storage.src.util.threadmanager import ThreadManager
from distributed.storage.src.util.service_thread import ServiceThread

def prepare_environment():
    path = os.path.abspath(__file__)
    print path
    path = path.split("/")
    print path
    path = "/".join(path[0:4])
    print "path", path
    sys.path.append(path)
    return True

def clean_db():
    # Cleaning DBs
    command = "rm -rf clientfile"
    try:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    return True

def start_client(mgmt_ip, mgmt_port, data_ip, data_port):

    id = "Server-" + str(random.randint(1,1000))
    controller_manager = ClientManager(id=id)
    controller_manager.start(mgmt_ip, mgmt_port, data_ip, data_port)
    return controller_manager

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.client.manager import ClientManager
    start_client(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    try:
        if sys.argv[5] != "persisted":
            clean_db()
    except:
        pass
    while True:
        continue
