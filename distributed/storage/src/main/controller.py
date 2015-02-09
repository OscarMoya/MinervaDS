import sys
import os

def prepare_environment():
    path = os.path.abspath(__file__)
    print path
    path = path.split("/")
    print path
    path = "/".join(path[0:4])
    print "path", path
    sys.path.append(path)

def start_controller(mgmt_ip, mgmt_port):

    controller_manager = ControllerManager()
    controller_manager.start(mgmt_ip, mgmt_port)
    return controller_manager

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.controller.manager import ControllerManager
    start_controller(sys.argv[1], int(sys.argv[2]))
    while True:
        continue




