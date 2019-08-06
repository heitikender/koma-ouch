import socket
from multiprocessing import Process
# from selfdrive.swaglog import cloudlog
import struct
import time

# Gets Engaged bool from ROS

class Server():
  def __init__(self):
    self.ENGAGED = False
    p = Process(target=self.start)

  def start(self, IP="192.168.200.20"):
    UDP_IP = IP
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    print 'UDP Engage Server is running on', UDP_IP, UDP_PORT
    while True:
      data, addr = sock.recvfrom(1) # buffer size is 1 byte and unpacks to bool
      ENGAGED = bool(struct.unpack('b', data)[0])
      print("Received message from address:", addr)
      print("Set Engaged to", ENGAGED)

  def getengaged(self):
    return self.ENGAGED