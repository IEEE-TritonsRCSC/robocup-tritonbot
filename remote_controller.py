from time import sleep
from interface.embedded_systems_interface import *
from tritonbot_message_processor.velocityConversions30 import * 
from analytics.plotter import *
from interface.pid import PID as pid
import sys

motorSpeed = 3000 
higherByte = (motorSpeed >> 8) & 0xff
lowerByte = motorSpeed & 0xff
print(motorSpeed)

pid1 = pid(5, 1, 0, 1000, 8000)
pid2 = pid(5, 1, 0, 1000, 8000)
pid3 = pid(5, 1, 0, 1000, 8000)
pid4 = pid(5, 1, 0, 1000, 8000)
pidValues = []

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

# 0xabc = 2748
# 0xf544 = -2748
forwards = bytes([0x11, 0x11, 0x0a, 0xbc, 0xf5, 0x44, 0x0a, 0xbc, 0xf5, 0x44])
backwards = bytes([0x11, 0x11, 0xf5, 0x44, 0x0a, 0xbc, 0xf5, 0x44, 0x0a, 0xbc])
left = bytes([0x11, 0x11, 0x0a, 0xbc, 0x0a, 0xbc, 0xf5, 0x44, 0xf5, 0x44])
right = bytes([0x11, 0x11, 0xf5, 0x44, 0xf5, 0x44, 0x0a, 0xbc, 0x0a, 0xbc])
clockwise = bytes([0x11, 0x11, 0xf5, 0x44, 0x0a, 0xbc, 0x0a, 0xbc, 0xf5, 0x44])
counterclockwise = bytes([0x11, 0x11, 0x0a, 0xbc, 0xf5, 0x44, 0xf5, 0x44, 0x0a, 0xbc])


'''Actions'''
reset = 0x00
dribble = 0x01
kick = 0x02
chip = 0x03

visuals = Plotter()
t=0


def moveCommands():
    control = input("Enter move command. WASDQE or nothing to stop\n").upper()
    if (control == "W"):
        sendToEmbedded(forwards)
    elif (control == "A"):
        sendToEmbedded(left)
    elif (control == "S"):
        sendToEmbedded(right)
    elif (control == "D"):
        sendToEmbedded(backwards)
    elif (control == "Q"):
        sendToEmbedded(counterclockwise)
    elif (control == "E"):
        sendToEmbedded(clockwise)
    else:
        stopAll()
    pass

try:
    while True:
        message = str(b'11110abc0abc0abc0abc')
         
        print(message)
        
        #moveCommands() 
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
            
            print(f"Wheel 1 PID output: {pid1.pid_calc(actualRpmArray[0])}")
            print(f"Wheel 2 PID output: {pid2.pid_calc(actualRpmArray[1])}")
            print(f"Wheel 3 PID output: {pid3.pid_calc(actualRpmArray[2])}")
            print(f"Wheel 4 PID output: {pid4.pid_calc(actualRpmArray[3])}")
         
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
    stopAll()
    print("stopped")
