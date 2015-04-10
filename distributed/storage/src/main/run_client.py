import os
import sys

ALLOWED_COMMANDS = ["upload", "download"]

def print_error(message):
    print "\033[1;31m%s\033[1;0m" % str(message)

def exit_on_error_args():
    sys.exit(print_error("Correct Usage: Available commands are %s (followed by data/pointer to file (uploads) or file id (dowloads)" % str(ALLOWED_COMMANDS)))


def initialise():
    import client_plain
    client = client_plain.get_client()
    return client

def upload_data(client, path_or_data):
    try:
        f = open(path_or_data, "rb")
        data = f.read()
        f.close()
    except:
        data = path_or_data
    upload_id = client.upload_file(data)
    # Clean up after sending data
    flows_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../..")
    try:
        for flow in ["a", "b", "c"]:
            flow_file = os.path.join(flows_location, "%s_flow_file" % flow)
            if os.path.isfile(flow_file):
                os.remove(flow_file)
    except Exception as e:
        print e
    return upload_id

def download_data(client, file_id):
    savedata = client.download_file(file_id)
    f = open("/tmp/minerva_ds__%s" % str(file_id), "w")
    f.write(savedata)
    f.close()
    return "File saved under %s" % str(f.name)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit_on_error_args()
    command = sys.argv[1]
    data = sys.argv[2]
    if command in ALLOWED_COMMANDS and data:
        client = initialise()
    else:
        sys.exit(print_error("Error: wrong input parameters"))
    if command == "upload":
        # Date is a path to a file or the full data
        print upload_data(client, data)
    elif command == "download":
        # Data is a file identifier
        print download_data(client, data)
    else:
        exit_on_error_args()
