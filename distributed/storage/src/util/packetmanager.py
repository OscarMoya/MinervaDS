from  distributed.storage.src.config.config import DSConfig
import subprocess

class PacketManager:

    @staticmethod
    def send_sync():
        command = PacketManager.generate_command_to_sync()
        try:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        except:
            subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        return True

    @staticmethod
    def generate_command_to_sync():
        magic_ip = DSConfig.MAGIC_IP
        packet_count = 1
        packet_size = 100
        command = "ping %s -c %d -s %d" %(magic_ip, packet_count, packet_size)
        return command


