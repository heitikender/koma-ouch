from multiprocessing import Process
import time
import socket
from udpclient import Client
import struct
class Server:
  def __init__(self, IP):
    self.steering = 0
    self.acceleration = 0
    self.p = Process(target=self.listen, args=[IP])
    self.p.start()
  def listen(self, IP="192.168.200.1"):
    UDP_IP = IP
    UDP_PORT = 5005
    self.sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    self.sock.bind((UDP_IP, UDP_PORT))
    print 'UDP Mock Server is running on', UDP_IP, UDP_PORT
    while True:
      data, addr = self.sock.recvfrom(8) # buffer size is 1 byte and unpacks to bool
      unpacked = struct.unpack('ff', data)
      self.steering = unpacked[0]
      self.acceleration = unpacked[1]
      print("Received message from address:", addr)
    #   print("Set Engaged to", ENGAGED)
  def stop(self):
    self.p.join()
  def getdata(self):
    print "Steering:", self.steering
    print "Acceleration:", self.acceleration

if __name__ == "__main__":
    s = Server("192.168.200.1")
    c = Client("192.168.200.20")
    # s = Server("127.0.0.1")
    # c = Client("127.0.0.1")
    z = True
    try:
        while(True):
            z = not z
            m = struct.pack('b', z)
            c.send_message(m)
            print "Sending", z
            print "5 seconds..."
            time.sleep(5)
            s.getdata()
            print "1 second..."
            time.sleep(5)
    except:
        pass
    print 'ending'
    s.stop()