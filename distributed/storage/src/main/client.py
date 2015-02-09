import sys
import os
import random

def prepare_environment():
    path = os.path.abspath(__file__)
    print path
    path = path.split("/")
    print path
    path = "/".join(path[0:4])
    print "path", path
    sys.path.append(path)

def start_client(mgmt_ip, mgmt_port, data_ip, data_port):

    id = "Server-" + str(random.randint(1,1000))
    controller_manager = ClientManager(id=id)
    controller_manager.start(mgmt_ip, mgmt_port, data_ip, data_port)
    return controller_manager

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.client.manager import ClientManager
    start_client(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    while True:
        continue