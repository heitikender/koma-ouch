import socket
class Client:
<<<<<<< Updated upstream
    def __init__(self):
        self.UDP_IP = "192.168.200.1"
        # self.UDP_IP = "127.0.0.1"
=======
    def __init__(self, IP = "192.168.200.1"):
        self.UDP_IP = IP
>>>>>>> Stashed changes
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
    def send_message(self, message):
<<<<<<< Updated upstream
        self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
=======
        self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))

# #Testing
# import struct
# c = Client("127.0.0.1")
# m = struct.pack('b', False)
# c.send_message(m)
# m = struct.pack('b', True)
# c.send_message(m)
# m = struct.pack('b', False)
# c.send_message(m)
>>>>>>> Stashed changes
