import sys
import os
import random
import subprocess

def prepare_environment():
    path = os.path.abspath(__file__)
    print path
    path = path.split("/")
    print path
    #path = "/".join(path[0:4])
    path = "/".join(path[0:3])
    print "path", path
    sys.path.append(path)

    #Cleaning DBs
    command = "rm -rf serverfile"
    try:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    return True

def start_server(mgmt_ip, mgmt_port, data_ip, data_port):

    id = "Server-" + str(random.randint(1,1000))
    controller_manager = ServerManager(id=id)
    controller_manager.start(mgmt_ip, mgmt_port, data_ip, data_port)
    return controller_manager

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.server.manager import ServerManager
    start_server(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    while True:
        continue
