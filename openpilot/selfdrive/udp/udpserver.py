import socket
# from selfdrive.swaglog import cloudlog
<<<<<<< Updated upstream
import time

# simple service that waits for network access and tries to update every hour

NICE_LOW_PRIORITY = ["nice", "-n", "19"]
def main(gctx=None):

=======
import struct
import time

# Gets Engaged bool from ROS

NICE_LOW_PRIORITY = ["nice", "-n", "19"]
ENGAGED = False

def getengaged():
  return ENGAGED

def main(gctx=None):
  global ENGAGED
>>>>>>> Stashed changes
  UDP_IP = "127.0.0.1"
  UDP_PORT = 5005

  sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
<<<<<<< Updated upstream
  while True:
    data, addr = sock.recvfrom(1) # buffer size is 1024 bytes
    print "received message:", data
    print "address:", addr

=======
  print 'UDP Engage Server is running on', UDP_IP, UDP_PORT
  while True:
    data, addr = sock.recvfrom(1) # buffer size is 1 byte and unpacks to bool
    ENGAGED = bool(struct.unpack('b', data)[0])
    print "Received message from address:", addr
    print "Set Engaged to", ENGAGED
>>>>>>> Stashed changes
if __name__ == "__main__":
  main()