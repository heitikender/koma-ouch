import struct

# TODO: Determine if needed and changes
def fix(msg, addr):
  checksum = 0
  idh = (addr & 0xff00) >> 8
  idl = (addr & 0xff)
  checksum = idh + idl + len(msg) + 1
  for d_byte in msg:
    checksum += ord(d_byte)
  #return msg + chr(checksum & 0xFF)
  return msg + struct.pack("B", checksum & 0xFF)


# TODO: Detemine changes
def make_can_msg(addr, dat, alt, cks=False):
  if cks:
    dat = fix(dat, addr)
  return [addr, 0, dat, alt]

# TODO: Determine if needed and changes
# def create_video_target(frame, addr):
#   counter = frame & 0xff
#   msg = struct.pack("!BBBBBBB", counter, 0x03, 0xff, 0x00, 0x00, 0x00, 0x00)
#   return make_can_msg(addr, msg, 1, True)

# TODO: Detemine changes
# def create_steer_command(packer, steer, steer_req, raw_cnt):
#   """Creates a CAN message for the Toyota Steer Command."""

#   values = {
#     "STEER_REQUEST": steer_req,
#     "STEER_TORQUE_CMD": steer,
#     "COUNTER": raw_cnt,
#     "SET_ME_1": 1,
#   }
#   return packer.make_can_msg("STEERING_LKA", 0, values)

# TODO: Detemine changes
# def create_accel_command(packer, accel, pcm_cancel, standstill_req, lead):
#   # TODO: find the exact canceling bit that does not create a chime
#   values = {
#     "ACCEL_CMD": accel,
#     "SET_ME_X01": 1,
#     "DISTANCE": 0,
#     "MINI_CAR": lead,
#     "SET_ME_X3": 3,
#     "SET_ME_1": 1,
#     "RELEASE_STANDSTILL": not standstill_req,
#     "CANCEL_REQ": pcm_cancel,
#   }
#   return packer.make_can_msg("ACC_CONTROL", 0, values)


# def create_fcw_command(packer, fcw):
#   values = {
#     "FCW": fcw,
#     "SET_ME_X20": 0x20,
#     "SET_ME_X10": 0x10,
#     "SET_ME_X80": 0x80,
#   }
#   return packer.make_can_msg("ACC_HUD", 0, values)
