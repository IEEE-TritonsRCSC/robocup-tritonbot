import serial
from time import sleep
from embedded_systems_interface import *

'''Move commands'''
front = bytes([])
back = bytes([])
left = bytes([])
right = bytes([])

'''Actions'''
reset = 0x00
dribble = 0x01
kick = 0x02
chip = 0x03


