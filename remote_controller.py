from time import sleep
from interface.embedded_systems_interface import *
from tritonbot_message_processor.velocityConversions30 import * 
from analytics.plotter import *
import sys

'''Move commands'''
wheel1 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
wheel2 = bytes([0x11, 0x11, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00])
wheel3 = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00])
wheel4 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc])
wheelAll = bytes([0x11, 0x11, 0x0a, 0xbc, 0x0a, 0xbc, 0x0a, 0xbc, 0x0a, 0xbc, ])

front = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
back = bytes([])
left = bytes([])
right = bytes([])

'''Actions'''
reset = 0x00
dribble = 0x01
kick = 0x02
chip = 0x03

while True:
    message = str(b'11110abc0abc0abc0abc')
        
    sendToEmbedded(wheelAll)

    actual_b = readFromEmbedded()
    
    t=0
    if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
        visuals = Plotter()
        expectedRpmArray = hexToRpmArray(4, str(message))
        actualRpmArray = hexToRpmArray(4, actual_b) 
        print(f"Expected: {expectedRpmArray}")
        print(f"Actual: {actualRpmArray}")
        visuals.update_plot(t, expectedRpmArray, actualRpmArray)
        t += 1	
