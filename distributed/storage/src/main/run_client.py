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
    return client.upload_file(data)

def download_data(client, file_id):
    return client.download_file(file_id)

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
