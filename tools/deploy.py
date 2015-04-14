import os
import paramiko
import subprocess
import sys
import time

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
    process_command = "python server.py " + ds_server_a_ip + " 9797 10.10.100.40 9696 >/dev/null 2>/dev/null &"
    start_server_a_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_a_ip, start_server_a_command)
    return server

def start_server_b():
    ds_server_b_ip = SERVER_B_IP
    process_command = "python server.py " + ds_server_b_ip + " 9797 10.10.100.50 9696 >/dev/null 2>/dev/null &"
    start_server_b_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_b_ip, start_server_b_command) 
    return server

def start_server_c():
    ds_server_c_ip = SERVER_C_IP
    process_command = "python server.py " + ds_server_c_ip + " 9797 10.10.100.10 9696 >/dev/null 2>/dev/null &"
    start_server_c_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    server = send_command_to_client(ds_server_c_ip, start_server_c_command)   
    return server

def start_controller_manager():
    ds_controller_ip = CONTROLLER_IP
    process_command = "python controller.py " + ds_controller_ip + " 9797 >/dev/null 2>/dev/null &"
    start_controller_manager_command = "cd /home/MinervaDS/distributed/storage/src/main/ && " + process_command
    controller = send_command_to_client(ds_controller_ip, start_controller_manager_command)
    return controller

def start_openflow_controller():
    ds_controller_ip = CONTROLLER_IP
    process_command = "python pox.py --verbose openflow.of_01 --port=6634 forwarding.rpf_app >/dev/null 2>/dev/null &"
    start_openflow_controller_command = "cd /home/pox/ && " + process_command
    controller = send_command_to_client(ds_controller_ip, start_openflow_controller_command)
    return controller

def start_upload(path_to_file=None):
    default_path_to_file = "/home/MinervaDS/toystory.avi"
    if path_to_file:
        default_path_to_file = path_to_file
    start_upload_command = "cd /home/MinervaDS/distributed/storage/src/main && python run_client.py upload %s" % str(default_path_to_file)
    return_code = subprocess.call(start_upload_command, shell = True)
    return return_code

def start_download(file_id):
    start_download_command = "cd /home/MinervaDS/distributed/storage/src/main && python run_client.py download %s" % str(file_id)
    return_code = subprocess.call(start_download_command, shell = True)
    return return_code

def modify_flow(modify_condition, flow = None):
    default_flow = "A"
    flow_server = {"A": SERVER_A_IP,
                        "AxB": SERVER_C_IP,
                        "B": SERVER_B_IP}
    flow_method = {"A": start_server_a,
                        "AxB": start_server_c,
                        "B": start_server_b}
    if flow in ["A", "AxB", "B"]:
        default_flow = flow
    flow_server_ip = flow_server[default_flow]
    if modify_condition == 1:
        # Stop the server in the selected location
        stop_pid(flow_server_ip, "python server.py")
    elif modify_condition == 0:
        # Start the server in the selected location
        server = flow_method[default_flow]()

def enable_flow(flow = None):
    modify_flow(0, flow)

def disable_flow(flow = None):
    modify_flow(1, flow)

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
    time.sleep(20)
    print "Starting OF controller manager"
    controller = start_controller_manager()
    time.sleep(1)
    print "Starting servers"
    server_a = start_server_a()
    server_b = start_server_b()
    server_c = start_server_c()
    print_info("...Done")

def restart_system():
    stop_system()
    print_info("Restarting OF controller manager")
    controller = start_controller_manager()
    time.sleep(1)
    print "Restarting servers"
    start_system()

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
    stop_system()

def error_and_exit(error_message=None):
    default_error_message = error_message
    if error_message:
        default_error_message = "Incorrect usage"
    print_error("%s: python %s" % (default_error_message, " ".join(sys.argv)))
    help()
    sys.exit(1)

def help():
    print_info("\nOperation parameters:")
    print "\tstart\t\t\tInitiate environment"
    print "\tstop\t\t\tStop environment"
    print "\tshutdown\t\tShutdown environment (stop + halt controller)"
    print "\trestart\t\t\tRestart environment (shutdown + start)"
    print "\thelp\t\t\tPrints help"
    print_info("\nTransmission parameters:")
    print "\tupload <file_path>\tStart upload of specific file"
    print "\t\t\t\tRequired argument: path to specific data file"
    print "\tdownload <file_id>\tStart download of file with specific identifier"
    print "\t\t\t\tRequired argument: file identifier (provided by \"upload\" operation)"
    print_info("\nFailure simulation parameters:")
    print "\tdisable [flow]\t\tDisable transmission of specific flow"
    print "\t\t\t\tOptional argument: specific flow (A, B, AxB). Default: A"
    print "\tenable [flow]\t\tEnable transmission of specific flow"
    print "\t\t\t\tOptional argument: specific flow (A, B, AxB). Default: A"

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        error_and_exit("Incorrect number of parameters")
    command = sys.argv[1]
    if command == "start":
        start_system()
    elif command == "stop":
        stop_system()
    elif command == "restart":
        restart_system()
    elif command == "shutdown":
        shut_down_system()
    elif command == "upload":
        if len(sys.argv) >= 3:
            start_upload(sys.argv[2])
        else:
            error_and_exit()
    elif command == "download":
        if len(sys.argv) >= 3:
            start_download(sys.argv[2])
        else:
            error_and_exit()
    elif command == "disable":
        if len(sys.argv) >= 3:
            disable_flow(sys.argv[2])
        else:
            disable_flow()
    elif command == "enable":
        if len(sys.argv) >= 3:
            enable_flow(sys.argv[2])
        else:
            enable_flow()
    elif command == "help":
        help()
    else:
        error_and_exit()
