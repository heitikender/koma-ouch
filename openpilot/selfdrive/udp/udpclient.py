import socket
class Client:
    def __init__(self):
        self.UDP_IP = "192.168.200.1"
        # self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
    def send_message(self, message):
        self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))