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
# import time
# c = Client("192.168.200.20")
# a = float(0)
# b = float(90)
# z = True
# while(True):
#     z = not z
#     m = struct.pack('b', z)
#     c.send_message(m)
#     print
#     print time.time()
#     print z
#     time.sleep(10)
