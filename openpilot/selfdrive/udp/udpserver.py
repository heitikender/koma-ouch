import socket
# from selfdrive.swaglog import cloudlog
import time

# simple service that waits for network access and tries to update every hour

NICE_LOW_PRIORITY = ["nice", "-n", "19"]
def main(gctx=None):

  UDP_IP = "127.0.0.1"
  UDP_PORT = 5005

  sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    data, addr = sock.recvfrom(1) # buffer size is 1024 bytes
    print "received message:", data
    print "address:", addr

if __name__ == "__main__":
  main()