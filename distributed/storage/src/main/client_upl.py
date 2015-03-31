import client_plain
import time
import subprocess

cl = client_plain.get_client()

time.sleep(6)

f = open("/home/MinervaDS/trailer.avi", "rb")
data = f.read()
f.close()
code = cl.upload_file(data, 2)

print code

time.sleep(8)

# Cleaning DBs
command = "rm -rf clientfile"
try:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
except:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

