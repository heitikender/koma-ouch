import struct
import numpy as np
from common.kalman.simple_kalman import KF1D
from selfdrive.can.can_define import CANDefine
from selfdrive.can.parser import CANParser
from selfdrive.config import Conversions as CV
from selfdrive.car.mitsubishi.values import CAR, DBC, STEER_THRESHOLD, NO_DSU_CAR
from selfdrive.udp.udpserver import Server

def parse_gear_shifter(gear, vals):

  val_to_capnp = {'P': 'park', 'R': 'reverse', 'N': 'neutral',
                  'D': 'drive', 'B': 'brake'}
  try:
    return val_to_capnp[vals[gear]]
  except KeyError:
    return "unknown"


def get_can_parser(CP):

  signals = [
    # sig_name, sig_address, default
    ("STEER_ANGLE", "STEER_ANGLE_SENSOR", 0),
    ("GEAR", "GEAR_PACKET", 0),
    ("SPEED", "COMBOMETER", 0),
  ]

  checks = [
    ("STEER_ANGLE_SENSOR", 20),
    ("MOTOR", 20),
  ]

  return CANParser(DBC[CP.carFingerprint]['pt'], signals, checks, 0)


class CarState(object):
  def __init__(self, CP):

    self.CP = CP
    self.can_define = CANDefine(DBC[CP.carFingerprint]['pt'])
    self.shifter_values = self.can_define.dv["GEAR_PACKET"]['GEAR']

     # initialize can parser
    self.car_fingerprint = CP.carFingerprint

    # vEgo kalman filter
    dt = 0.01
    # Q = np.matrix([[10.0, 0.0], [0.0, 100.0]])
    # R = 1e3
    self.v_ego_kf = KF1D(x0=[[0.0], [0.0]],
                         A=[[1.0, dt], [0.0, 1.0]],
                         C=[1.0, 0.0],
                         K=[[0.12287673], [0.29666309]])
    self.v_ego = 0.0

  def update(self, cp):

    # update prevs, update must run once per loop
#     self.prev_left_blinker_on = self.left_blinker_on
#     self.prev_right_blinker_on = self.right_blinker_on

#     self.door_all_closed = not any([cp.vl["SEATS_DOORS"]['DOOR_OPEN_FL'], cp.vl["SEATS_DOORS"]['DOOR_OPEN_FR'],
#                                     cp.vl["SEATS_DOORS"]['DOOR_OPEN_RL'], cp.vl["SEATS_DOORS"]['DOOR_OPEN_RR']])
#     self.seatbelt = not cp.vl["SEATS_DOORS"]['SEATBELT_DRIVER_UNLATCHED']

#     self.brake_pressed = cp.vl["BRAKE_MODULE"]['BRAKE_PRESSED']
#     if self.CP.enableGasInterceptor:
#       self.pedal_gas = (cp.vl["GAS_SENSOR"]['INTERCEPTOR_GAS'] + cp.vl["GAS_SENSOR"]['INTERCEPTOR_GAS2']) / 2.
#     else:
    self.pedal_gas = 0 #cp.vl["GAS_PEDAL"]['GAS_PEDAL']
#     self.car_gas = self.pedal_gas
#     self.esp_disabled = cp.vl["ESP_CONTROL"]['TC_DISABLED']

    # # calc best v_ego estimate, by averaging two opposite corners
    # self.v_wheel_fl = cp.vl["ABS_FRONT"]['WHEEL_SPEED_FL'] * CV.KPH_TO_MS
    # self.v_wheel_fr = cp.vl["ABS_FRONT"]['WHEEL_SPEED_FR'] * CV.KPH_TO_MS
    # self.v_wheel_rl = cp.vl["ABS_REAR"]['WHEEL_SPEED_RL'] * CV.KPH_TO_MS
    # self.v_wheel_rr = cp.vl["ABS_REAR"]['WHEEL_SPEED_RR'] * CV.KPH_TO_MS
    v_wheel = cp.vl["COMBOMETER"]['SPEED'] * CV.KPH_TO_MS

    # Kalman filter
    if abs(v_wheel - self.v_ego) > 2.0:  # Prevent large accelerations when car starts at non zero speed
      self.v_ego_kf.x = [[v_wheel], [0.0]]

    self.v_ego_raw = v_wheel
    v_ego_x = self.v_ego_kf.update(v_wheel)
    self.v_ego = float(v_ego_x[0])
    self.a_ego = float(v_ego_x[1])
    self.standstill = not v_wheel > 0.001

    self.angle_steers = cp.vl["STEER_ANGLE_SENSOR"]['STEER_ANGLE']
    self.angle_steers_rate = cp.vl["STEER_ANGLE_SENSOR"]['STEER_RATE']
    can_gear = int(cp.vl["GEAR_PACKET"]['GEAR'])
    self.gear_shifter = parse_gear_shifter(can_gear, self.shifter_values)
    self.main_on = True #cp.vl["PCM_CRUISE_2"]['MAIN_ON']
#     self.left_blinker_on = cp.vl["STEERING_LEVERS"]['TURN_SIGNALS'] == 1
#     self.right_blinker_on = cp.vl["STEERING_LEVERS"]['TURN_SIGNALS'] == 2

#     # 2 is standby, 10 is active. TODO: check that everything else is really a faulty state
    self.steer_state = 3 #cp.vl["EPS_STATUS"]['LKA_STATE']
    self.steer_error = False #cp.vl["EPS_STATUS"]['LKA_STATE'] not in [1, 5]
#     self.ipas_active = cp.vl['EPS_STATUS']['IPAS_STATE'] == 3
    self.brake_error = 0
    self.steer_torque_driver = 0 #cp.vl["STEER_TORQUE_SENSOR"]['STEER_TORQUE_DRIVER']
    self.steer_torque_motor = 0 #cp.vl["STEER_TORQUE_SENSOR"]['STEER_TORQUE_EPS']
#     # we could use the override bit from dbc, but it's triggered at too high torque values
    self.steer_override = False #abs(self.steer_torque_driver) > STEER_THRESHOLD

    self.user_brake = 0

    #cruise control
    if not self.pcm_acc_active:
      self.v_cruise_pcm = cp.vl["COMBOMETER"]['SPEED']
    self.pcm_acc_status = 8 # cp.vl["PCM_CRUISE"]['CRUISE_STATE'] # 8
    self.pcm_acc_active = Server.getengaged()
    self.brake_lights = bool(cp.vl["ESP_CONTROL"]['BRAKE_LIGHTS_ACC'] or self.brake_pressed)
