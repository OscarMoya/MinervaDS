import sys
import os
import subprocess

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
    command = "rm -rf controllerendpoint controllerlocation"
    try:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    return True

def start_controller(mgmt_ip, mgmt_port):

    controller_manager = ControllerManager()
    controller_manager.start(mgmt_ip, mgmt_port)
    return controller_manager

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.controller.manager import ControllerManager
    start_controller(sys.argv[1], int(sys.argv[2]))
    try:
        if sys.argv[3] != "persisted":
            clean_db()
    except:
        pass
    while True:
        continue
