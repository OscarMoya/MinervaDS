import os
import paramiko
import sys

def print_error(message):
    print "\033[1;31m%s\033[1;0m" % str(message)

def print_info(message):
    print "\033[0;34m%s\033[1;0m" % str(message)

try:
    from deploy_config import *
    deploy_vars = [SERVER_A_IP, SERVER_B_IP, SERVER_C_IP, CONTROLLER_IP, SSH_PASSWORD, SSH_PORT]
    if any((x is None for x in deploy_vars)):
        raise Exception
except:
    sys.exit(print_error("Error: deploy_config.py not available or configured incorrectly"))

def get_ssh_client_and_connect(ip):
    client =  paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username="root", port = SSH_PORT, password = SSH_PASSWORD)
    return client

def start_server_a():
    ds_server_a_ip = SERVER_A_IP
    process_command = "python server.py " + ds_server_a_ip + " 9797 10.10.100.40 9696"
    start_server_a_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_a_ip, start_server_a_command)
    return server

def start_server_b():
    ds_server_b_ip = SERVER_B_IP
    process_command = "python server.py " + ds_server_b_ip + " 9797 10.10.100.50 9696"
    start_server_b_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_b_ip, start_server_b_command) 
    return server

def start_server_c():
    ds_server_c_ip = SERVER_C_IP
    process_command = "python server.py " + ds_server_c_ip + " 9797 10.10.100.10 9696"
    start_server_c_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_c_ip, start_server_c_command)   
    return server

def start_controller_manager():
    ds_controller_ip = CONTROLLER_IP
    process_command = "python controller.py " + ds_controller_ip + " 9797"
    start_controller_manager_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    controller = send_command_to_client(ds_controller_ip, start_controller_manager_command)
    return controller

def start_openflow_controller():
    ds_controller_ip = CONTROLLER_IP
    process_command = "python pox.py --verbose openflow.of_01 --port=6634 forwarding.rpf_app >/dev/null 2>/dev/null &"
    start_openflow_controller_command = "cd /home/pox/ && " + process_command
    controller = send_command_to_client(ds_controller_ip, start_openflow_controller_command)
    return controller

def send_command_to_client(ip, command):
    client = get_ssh_client_and_connect(ip)
    a,b,c = client.exec_command(command)
    return client

def stop_pid_command(process_name):
    return "kill -9 $(ps aux | grep '" + process_name + "' | awk '{print $2}')"

def stop_pid(ip, process_name):
    shell = get_ssh_client_and_connect(ip)
    a,b,c = shell.exec_command(stop_pid_command(process_name))

def stop_pid_local(process_name):
    os.system(stop_pid_command(process_name))

def start_system():
    print_info("Starting system...")
    print "Starting OF controller"
    start_openflow_controller()
    print "Starting OF controller manager"
    controller = start_controller_manager()
    print "Starting servers"
    server_a = start_server_a()
    server_b = start_server_b()
    server_c = start_server_c()
    print_info("...Done")

def restart_system():
    stop_system()
    print_info("Restarting OF controller manager")
    controller = start_controller_manager()
    print "Restarting servers"
    server_a = start_server_a()
    server_b = start_server_b()
    server_c = start_server_c()
    print_info("...Done")

def stop_system():
    print_info("Stopping system...")
    print "Stopping OF controller manager"
    stop_pid(CONTROLLER_IP, "python controller.py")
    print "Stopping servers"
    stop_pid(SERVER_A_IP, "python server.py")
    stop_pid(SERVER_B_IP, "python server.py")
    stop_pid(SERVER_C_IP, "python server.py")
    print_info("...Done")

def shut_down_system():
    print_info("Shutting system down...")
    print "Shutting down OF controller"
    stop_pid(CONTROLLER_IP, "python pox.py")
    print "Shutting down OF controller manager"
    stop_pid(CONTROLLER_IP, "python controller.py")
    print "Shutting down servers"
    stop_pid(SERVER_A_IP, "python server.py")
    stop_pid(SERVER_B_IP, "python server.py")
    stop_pid(SERVER_C_IP, "python server.py")
    print_info("...Done")

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "start":
        start_system()
    elif command == "stop":
        stop_system()
    elif command == "restart":
        restart_system()
    elif command == "shutdown":
        shut_down_system()
    else:
        print_error("Correct Usage: Available commands are start, stop, restart, shutdown")
