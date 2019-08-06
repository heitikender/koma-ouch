import socket
class Client:
    def __init__(self, IP = "192.168.200.1"):
        self.UDP_IP = IP
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
    def send_message(self, message):
        self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))

# #Testing
# import struct
# c = Client()
# a = float(0)
# b = float90
# while(True):
#     a += 1
#     b += 10
#     m = struct.pack('ff', a, b)
#     c.send_message(m)
