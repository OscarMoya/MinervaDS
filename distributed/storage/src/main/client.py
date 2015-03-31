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

def logger_thread(message, log_file="/home/MinervaDS/client_perf.txt"):
    if os.path.exists(log_file):
        l = open(log_file, 'a')
        l.write(message+"\n")

    else:
        l = open(log_file, 'wb')
        l.write(message+"\n")
    l.close()

def prepare_environment():
    path = os.path.abspath(__file__)
    print path
    path = path.split("/")
    print path
    path = "/".join(path[0:4])
    print "path", path
    sys.path.append(path)

    #Cleaning DBs
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
    from distributed.storage.src.module.client.manager import ClientManager
    start_client(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    #pid = os.getpid()
    #ThreadManager.start_method_in_new_thread(timer, [pid])
    while True:
        continue
