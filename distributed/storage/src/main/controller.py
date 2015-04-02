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

def logger(message):
    ServiceThread.start_in_new_thread(logger_thread, message)

def logger_thread(message, log_file="/home/MinervaDS/controller_perf.txt"):
    if os.path.exists(log_file):
        l = open(log_file, 'a')
        l.write(message+"\n")

    else:
        l = open(log_file, 'wb')
        l.write(message+"\n")
    l.close()

def prepare_environment():
    path = os.path.abspath(__file__)
    path = path.split("/")
    path = "/".join(path[0:3])
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

def timer(pid):
    try:
        while True:
            x = get_cpumem(pid)
            if not x:
                print("no such process")
                exit(1)
            message = "%.2f\t%.2f" % x
            logger(message)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print
        exit(0)

def get_cpumem(pid):
    d = [i for i in commands.getoutput("ps aux").split("\n")
        if i.split()[1] == str(pid)]
    return (float(d[0].split()[2]), float(d[0].split()[3])) if d else None

if __name__ == "__main__":
    prepare_environment()
    from distributed.storage.src.module.controller.manager import ControllerManager
    start_controller(sys.argv[1], int(sys.argv[2]))
    #pid = os.getpid()
    #ThreadManager.start_method_in_new_thread(timer, [pid])
    try:
        if sys.argv[3] != "persisted":
            clean_db()
    except:
        pass
    while True:
        continue

