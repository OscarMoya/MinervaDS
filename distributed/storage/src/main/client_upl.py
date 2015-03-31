import client_plain
import time
import subprocess

cl = client_plain.get_client()

time.sleep(6)

f = open("/home/MinervaDS/trailer.avi", "rb")
data = f.read()
f.close()
code = cl.upload_file(data, 2)


#code = cl.upload_file("HELLO WORLD!", 2)

print code

time.sleep(8)

"""
while True:
    #print "Uploading..."
    print "Downloading..."
   
    #Cleaning DBs
    command = "rm -rf clientfile"
    try:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    #cl.upload_file("HELLO WORLD!", 2)
    #cl.download_file('276b2050-27ae-4c56-aae5-da10f89f7b20')
    cl.download_file(code[1])
   
    f = open("/home/MinervaDS/sample.jpg", "rb")
    data = f.read()
    f.close()
    cl.upload_file(data, 2)
   
    time.sleep(10)
"""
"""
#cl.upload_file("HELLO WORLD!", 2)

f = open("/home/MinervaDS/sample.jpg", "rb")
data = f.read()
f.close()

print "Uploading..."
cl.upload_file(data, 2)
"""
#Cleaning DBs
command = "rm -rf clientfile"
try:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
except:
    subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
"""
print "Downloading..."

cl.download_file(code[1])
"""
