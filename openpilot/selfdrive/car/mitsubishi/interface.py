#!/usr/bin/env python
from common.realtime import sec_since_boot
from cereal import car
from selfdrive.config import Conversions as CV
from selfdrive.controls.lib.drive_helpers import EventTypes as ET, create_event
from selfdrive.controls.lib.vehicle_model import VehicleModel
from selfdrive.car.mitsubishi.carstate import CarState, get_can_parser
from selfdrive.car.mitsubishi.values import ECU, check_ecu_msgs, CAR
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness
from selfdrive.swaglog import cloudlog

class CarInterface(object):
   def __init__(self, CP, CarController):
     self.CP = CP
     self.VM = VehicleModel(CP)

     self.frame = 0
     self.gas_pressed_prev = False
     self.brake_pressed_prev = False
     self.cruise_enabled_prev = False

     # *** init the major players ***
     self.CS = CarState(CP)

     self.cp = get_can_parser(CP)
     self.cp_cam = get_cam_can_parser(CP)

     self.forwarding_camera = False

     self.CC = None
     if CarController is not None:
       self.CC = CarController(self.cp.dbc_name, CP.carFingerprint, CP.enableCamera, CP.enableDsu, CP.enableApgs)

   @staticmethod
   def compute_gb(accel, speed):
     return float(accel) / 3.0

   @staticmethod
   def calc_accel_override(a_ego, a_target, v_ego, v_target):
     return 1.0

   @staticmethod
   def get_params():

    ret = car.CarParams.new_message()

    ret.carName = "mitsubichi"
    ret.carFingerprint = "MITSUBISHI MIEV"
    ret.carVin = ""
    ret.isPandaBlack = False

    ret.safetyModel = car.CarParams.SafetyModel.toyota

    # # pedal
    # ret.enableCruise = not ret.enableGasInterceptor

    ret.steerActuatorDelay = 0.1  # Default delay
    ret.lateralTuning.init('pid')
    ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
    ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.01], [0.005]]
    ret.lateralTuning.pid.kf = 0.001388889 # 1 / max angle
    ret.steerRateCost = 1.0
    ret.centerToFront = ret.wheelbase * 0.44
    tire_stiffness_factor = 0.5328
    ret.min_EnableSpeed = 1

    ret.enableCamera = False #not check_ecu_msgs(fingerprint, ECU.CAM) or is_panda_black
    ret.enableDsu = not check_ecu_msgs(fingerprint, ECU.DSU)
    ret.enableApgs = False #not check_ecu_msgs(fingerprint, ECU.APGS)
    ret.openpilotLongitudinalControl = ret.enableCamera and ret.enableDsu
    cloudlog.warn("ECU DSU Simulated: %r", ret.enableDsu)


    ret.longitudinalTuning.deadzoneBP = [0., 9.]
    ret.longitudinalTuning.deadzoneV = [0., .15]
    ret.longitudinalTuning.kpBP = [0., 5., 35.]
    ret.longitudinalTuning.kiBP = [0., 35.]
    ret.stoppingControl = False
    ret.startAccel = 0.0

    ret.gasMaxBP = [0., 9., 35]
    ret.gasMaxV = [0.2, 0.5, 0.7]
    ret.longitudinalTuning.kpV = [1.2, 0.8, 0.5]
    ret.longitudinalTuning.kiV = [0.18, 0.12]

    return ret

   # returns a car.CarState
   def update(self, c, can_strings):
     # ******************* do can recv *******************
     self.cp.update_strings(int(sec_since_boot() * 1e9), can_strings)


     self.CS.update(self.cp)

     # create message
     ret = car.CarState.new_message()

     ret.canValid = self.cp.can_valid

     # speeds
     ret.vEgo = self.CS.v_ego
     ret.vEgoRaw = self.CS.v_ego_raw
     ret.aEgo = self.CS.a_ego
     ret.yawRate = self.VM.yaw_rate(self.CS.angle_steers * CV.DEG_TO_RAD, self.CS.v_ego)
     ret.standstill = self.CS.standstill

     # gear shifter
     ret.gearShifter = self.CS.gear_shifter

     # gas pedal
     ret.gas = self.CS.car_gas
     ret.gasPressed = self.CS.pedal_gas > 0

     # brake pedal
     ret.brake = self.CS.user_brake
     ret.brakePressed = self.CS.brake_pressed != 0
     ret.brakeLights = self.CS.brake_lights

     # steering wheel
     ret.steeringAngle = self.CS.angle_steers
     ret.steeringRate = self.CS.angle_steers_rate

     ret.steeringTorque = self.CS.steer_torque_driver
     ret.steeringPressed = self.CS.steer_override

     # cruise state
     ret.cruiseState.enabled = self.CS.pcm_acc_active
     ret.cruiseState.speed = self.CS.v_cruise_pcm * CV.KPH_TO_MS
     ret.cruiseState.available = bool(self.CS.main_on)
     ret.cruiseState.speedOffset = 0.

     ret.doorOpen = False #not self.CS.door_all_closed
     ret.seatbeltUnlatched = False #not self.CS.seatbelt

     # events
     events = []

#     if not ret.gearShifter == 'drive' and self.CP.enableDsu:
#       events.append(create_event('wrongGear', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
#     if ret.doorOpen:
#       events.append(create_event('doorOpen', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
#     if ret.seatbeltUnlatched:
#       events.append(create_event('seatbeltNotLatched', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
#     if self.CS.esp_disabled and self.CP.enableDsu:
#       events.append(create_event('espDisabled', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
#     if not self.CS.main_on and self.CP.enableDsu:
#       events.append(create_event('wrongCarMode', [ET.NO_ENTRY, ET.USER_DISABLE]))
#     if ret.gearShifter == 'reverse' and self.CP.enableDsu:
#       events.append(create_event('reverseGear', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))
#     if self.CS.steer_error:
#       events.append(create_event('steerTempUnavailable', [ET.NO_ENTRY, ET.WARNING]))
#     if self.CS.low_speed_lockout and self.CP.enableDsu:
#       events.append(create_event('lowSpeedLockout', [ET.NO_ENTRY, ET.PERMANENT]))
#     if ret.vEgo < self.CP.minEnableSpeed and self.CP.enableDsu:
#       events.append(create_event('speedTooLow', [ET.NO_ENTRY]))
#       if c.actuators.gas > 0.1:
#         # some margin on the actuator to not false trigger cancellation while stopping
#         events.append(create_event('speedTooLow', [ET.IMMEDIATE_DISABLE]))
#       if ret.vEgo < 0.001:
#         # while in standstill, send a user alert
#         events.append(create_event('manualRestart', [ET.WARNING]))

     ret.events = events

     self.gas_pressed_prev = ret.gasPressed
     self.brake_pressed_prev = ret.brakePressed
     self.cruise_enabled_prev = ret.cruiseState.enabled

     return ret.as_reader()

   # pass in a car.CarControl
   # to be called @ 100hz
   def apply(self, c):

     can_sends = self.CC.update(c.enabled, self.CS, self.frame,
                                c.actuators, c.cruiseControl.cancel, c.hudControl.visualAlert,
                                c.hudControl.audibleAlert, self.forwarding_camera,
                                c.hudControl.leftLaneVisible, c.hudControl.rightLaneVisible, c.hudControl.leadVisible,
                                c.hudControl.leftLaneDepart, c.hudControl.rightLaneDepart)

     self.frame += 1
     return can_sends
