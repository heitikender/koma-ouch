import os
from cereal import car
from common.params import Params
from common.vin import get_vin, VIN_UNKNOWN
from common.basedir import BASEDIR
from selfdrive.swaglog import cloudlog
import selfdrive.messaging as messaging
from selfdrive.car.mitsubishi.carcontroller import CarController
from selfdrive.car.mitsubishi.interface import CarInterface


def get_startup_alert(car_recognized, controller_available):
  alert = 'startup'
  if not car_recognized:
    alert = 'startupNoCar'
  elif car_recognized and not controller_available:
    alert = 'startupNoControl'
  return alert

#return interfaces for mitsubishi miev only
def get_car(logcan, sendcan, is_panda_black=False):

  candidate = "MITSUBISHI MIEV"
  vin = "xxxxxxxxxxxx"
  car_params = CarInterface.get_params()

  return CarInterface(car_params, CarController), car_params
