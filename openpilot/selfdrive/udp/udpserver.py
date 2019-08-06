import socket
# from selfdrive.swaglog import cloudlog
import struct
import time

# Gets Engaged bool from ROS

NICE_LOW_PRIORITY = ["nice", "-n", "19"]
ENGAGED = False

def getengaged():
  return ENGAGED

def main(gctx=None):
  global ENGAGED
  UDP_IP = "192.168.200.20"
  UDP_PORT = 5005

  sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  print 'UDP Engage Server is running on', UDP_IP, UDP_PORT
  while True:
    data, addr = sock.recvfrom(1) # buffer size is 1 byte and unpacks to bool
    print data
    ENGAGED = bool(struct.unpack('b', data)[0])
    print "Received message from address:", addr
    print "Set Engaged to", ENGAGED
if __name__ == "__main__":
  main()