########################################################################################################################
#
#                               Pacemaker class for communicating with pacemaker
#
########################################################################################################################
import serial
from struct import *
from time import sleep


ser = serial.Serial("COM3", 115200)

GET_ID = Struct("2I", 11001) #getID code (25)
GET_PARAMS = Struct()

def get_device_id(self):
        ser.write(GET_ID)
        ser.read()

class Pacemaker:
    def __init__(self, ID):
        device_id = ID
    def get_id(self):
         return (self.ID)
    def get_params():
         
    