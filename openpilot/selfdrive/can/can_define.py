from collections import defaultdict
from selfdrive.can.libdbc_py import libdbc, ffi

class CANDefine(object):
  def __init__(self, dbc_name):
    print "dbc_name:", dbc_name
    self.dv = defaultdict(dict)
    print 1
    self.dbc_name = dbc_name
    print 2
    self.dbc = libdbc.dbc_lookup(dbc_name)
    print "dbc:", self.dbc
    num_vals = self.dbc[0].num_vals
    print "num_vals", num_vals
    self.address_to_msg_name = {}
    num_msgs = self.dbc[0].num_msgs
    print "num_msgs:", num_msgs
    print "num_msgs loop..."
    for i in range(num_msgs):
      msg = self.dbc[0].msgs[i]
      print "msg:", msg
      name = ffi.string(msg.name)
      print "name:", name
      address = msg.address
      print "address", address
      self.address_to_msg_name[address] = name

    print "num_vals loop..."
    for i in range(num_vals):
      val = self.dbc[0].vals[i]
      print "val:", val
      sgname = ffi.string(val.name)
      print "sgname:", sgname
      address = val.address
      print "address:", address
      def_val = ffi.string(val.def_val)

      #separate definition/value pairs
      def_val = def_val.split()
      values = [int(v) for v in def_val[::2]]
      defs = def_val[1::2]

      if address not in self.dv:
        self.dv[address] = {}
        msgname = self.address_to_msg_name[address]
        self.dv[msgname] = {}

      # two ways to lookup: address or msg name
      self.dv[address][sgname] = {v: d for v, d in zip(values, defs)} #build dict
      self.dv[msgname][sgname] = self.dv[address][sgname]
    print "CANDefine done"
