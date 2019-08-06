import socket
from multiprocessing import Process
# from selfdrive.swaglog import cloudlog
import struct
import time

# Gets Engaged bool from ROS

class Server:
  def __init__(self, IP="192.168.200.20"):
    self.ENGAGED = False
    self.UDP_IP = IP
    self.UDP_PORT = 5005
    self.p = Process(target=self.listen)
    self.p.start()
  def listen(self, IP="192.168.200.20"):

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((self.UDP_IP, self.UDP_PORT))
    print 'UDP Engage Server is running on', self.UDP_IP, self.UDP_PORT
    while True:
      data, addr = sock.recvfrom(1) # buffer size is 1 byte and unpacks to bool
      ENGAGED = bool(struct.unpack('b', data)[0])
      print("Received message from address:", addr)
      print("Set Engaged to", self.ENGAGED)
  def stop(self):
    self.p.join()
  def getengaged(self):
    return self.ENGAGED

#Testing
# s = Server()
# try:
#   while(True):
#     time.sleep()
#     print s.getengaged()
# except:
#   pass
# s.stop()
