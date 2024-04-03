from time import sleep
from interface.embedded_systems_interface import *
from tritonbot_message_processor.velocityConversions30 import * 
from analytics.plotter import *
from tritonbot_message_processor.pid import PID as pid
import binascii
import sys

wheelSpeed = 7000
motorSpeed = [-wheelSpeed, -wheelSpeed, wheelSpeed, wheelSpeed] 

p=0.1
pid1 = pid(p, 0, 0, 1000, 8000)
pid2 = pid(p, 0, 0, 1000, 8000)
pid3 = pid(p, 0, 0, 1000, 8000)
pid4 = pid(p, 0, 0, 1000, 8000)

'''Move commands'''

wheel1 = bytes([0x11, 0x11, 0x8a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
wheel1I = bytes([0x11, 0x11, 0x7a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

wheel2 = bytes([0x11, 0x11, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00])
wheel3 = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00])
wheel4 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc])
wheelAll = bytes([0x11, 0x11, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8])

velocities = [0x11, 0x11] + rpmArrayToHex(motorSpeed)
print(velocities)
velocities = bytes(velocities)



stop = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

kick = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x14])

# 0xabc = 2748
# 0xf544 = -2748
left = bytes([0x11, 0x11, 0x0a, 0xbc, 0xf5, 0x44, 0x0a, 0xbc, 0xf5, 0x44])
right = bytes([0x11, 0x11, 0xf5, 0x44, 0x0a, 0xbc, 0xf5, 0x44, 0x0a, 0xbc])
backwards = bytes([0x11, 0x11, 0x0a, 0xbc, 0x0a, 0xbc, 0xf5, 0x44, 0xf5, 0x44])
forwards = bytes([0x11, 0x11, 0xe0, 0xc0, 0xe0, 0xc0, 0x1f, 0x40, 0x1f, 0x40])
clockwise = bytes([0x11, 0x11, 0xf5, 0x44, 0x0a, 0xbc, 0x0a, 0xbc, 0xf5, 0x44])
counterclockwise = bytes([0x11, 0x11, 0x0a, 0xbc, 0xf5, 0x44, 0xf5, 0x44, 0x0a, 0xbc])


'''Actions'''
reset = 0x00
dribble = 0x01
# kick = 0x02
chip = 0x03

#visuals = Plotter()
t=0


def moveCommands():
    control = input("Enter move command. WASD, QE, K, or nothing to stop\n").upper()
    if (control == "K"):
        sendToEmbedded(kick)
        print(f"Sent: {kick}")
        print(readFromEmbedded())
    elif (control == "W"):
        sendToEmbedded(forwards)
        print(f"Sent: {forwards}")
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
        sendToEmbedded(stop)
    pass

try:
    while True:
        if (len(sys.argv) == 1):
            moveCommands()
        
        elif (len(sys.argv) > 1 and sys.argv[1] == "-a"):
            #velocities = [0x11, 0x11] + rpmArrayToHex(motorSpeed)
            #velocities = bytes(velocities)
            
            # Comment the following lines to prevent sending 
            if len(sys.argv) == 2:
                sendToEmbedded(velocities)
                print(f"Data sent: {velocities}")

            actual_b = readFromEmbedded()
            print(f"Raw data received: {actual_b}")
            if str(actual_b) == "None":
                print("NOTHING RECEIVED")
                continue
            
            # visuals = Plotter()
            expectedRpmArray = hexToRpmArray(4, binascii.hexlify(velocities).decode()) #[motorSpeed, motorSpeed, motorSpeed, motorSpeed])
            actualRpmArray = hexToRpmArray(8, actual_b) 
            

            
            pidValues = []
            motorSpeed[0] = int(pid1.pid_calc(actualRpmArray[0]))
            #print(f"Wheel 1 PID output: {pidValues[0]}")
            motorSpeed[1] = int(pid2.pid_calc(actualRpmArray[1]))
            #print(f"Wheel 2 PID output: {pidValues[1]}")
            motorSpeed[2] = int(pid3.pid_calc(actualRpmArray[2]))
            #print(f"Wheel 3 PID output: {pidValues[2]}")
            motorSpeed[3] = int(pid4.pid_calc(actualRpmArray[3]))
            #print(f"Wheel 4 PID output: {pidValues[3]}")
            
            print(f"Expected velocities: {expectedRpmArray}")
            
            print(f"Actual (received): {actualRpmArray}")
            #visuals.update_plot(t, expectedRpmArray, actualRpmArray)
            
            # velocities = bytes([0x11, 0x11] + rpmArrayToHex(pidValues))
            #print(f"New PID values (motor speeds?): {motorSpeed}")
            if t%99999 == 99994:
                print("Set new PID values:\n")
                print("Set new PID values:\n")
                Kp = (input("New kP (Press enter to skip): "))

                if (Kp != ""):
                    Kp = float(Kp)
                    Ki = float(input("New kI: "))
                    Kd = float(input("New kD: "))
                    pid1.set_pid_constants(Kp, Kd, Ki)
                    pid2.set_pid_constants(Kp, Kd, Ki)
                    pid3.set_pid_constants(Kp, Kd, Ki)
                    pid4.set_pid_constants(Kp, Kd, Ki)
                
            t += 1
            	
        else:
            print("Invalid command args. Crtl + C to terminate")
		
except KeyboardInterrupt:
    if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
        stopAll()
        print("\nProgram terminated.")
        visuals.save()

finally:
    stopAll()
