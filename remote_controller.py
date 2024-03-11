from time import sleep
from interface.embedded_systems_interface import *
from tritonbot_message_processor.velocityConversions30 import * 
from analytics.plotter import *
import sys

motorSpeed = 5000 
higherByte = (motorSpeed >> 8) & 0xff
lowerByte = motorSpeed & 0xff
print(motorSpeed)

'''Move commands'''
wheel1 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
wheel2 = bytes([0x11, 0x11, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00])
wheel3 = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00])
wheel4 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc])
wheelAll = bytes([0x11, 0x11, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8])

velocities = [0x11, 0x11]
for i in range(4):
    velocities.append(motorSpeed>>8 & 0xff)
    velocities.append(motorSpeed & 0xff)
print(bytes(velocities))

velocities = bytes(velocities)



stop = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

front = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
back = bytes([])
left = bytes([])
right = bytes([])

'''Actions'''
reset = 0x00
dribble = 0x01
kick = 0x02
chip = 0x03

visuals = Plotter()
t=0

try:
    while True:
        message = str(b'11110abc0abc0abc0abc')
         
        print(message)
            
        sendToEmbedded(velocities)

        actual_b = readFromEmbedded()
        print(actual_b)
        if str(actual_b) == "None":
            print("NOTHING RECEIVED")
            continue
            actual_b = "11110000000000000000"
        
        
        if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
            # visuals = Plotter()
            expectedRpmArray = hexToRpmArray(6, message)#[motorSpeed, motorSpeed, motorSpeed, motorSpeed])
            actualRpmArray = hexToRpmArray(8, actual_b) 
            
            print(f"Expected: {expectedRpmArray}")
            
            print(f"Actual: {actualRpmArray}")
            visuals.update_plot(t, expectedRpmArray, actualRpmArray)
            t += 1	

		
except KeyboardInterrupt:
    stopAll()
    print("\nProgram terminated.")
    save = input("Graph plotted. Save to png? (Y/n)\n").upper()

    if save == 'Y':
        saveName = input("What would you like to name this file?\n")
        visuals.save(saveName)



finally:
    print("stopped")
