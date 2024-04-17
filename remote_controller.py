from time import sleep
from interface.embedded_systems_interface import *
from tritonbot_message_processor.velocityConversions30 import * 
#from analytics.plotter import *
from tritonbot_message_processor.pid import PID as pid
import binascii
import sys

wheelSpeed = 300
motorSpeed = [wheelSpeed, wheelSpeed, wheelSpeed, wheelSpeed] 

pid1 = pid(10, 0, 0, 1000, 8000)
pid2 = pid(10, 0, 0, 1000, 8000)
pid3 = pid(10, 0, 0, 1000, 8000)
pid4 = pid(10, 0, 0, 1000, 8000)

'''Move commands'''
wheel1 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
wheel2 = bytes([0x11, 0x11, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00])
wheel3 = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc, 0x00, 0x00])
wheel4 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xbc])
wheelAll = bytes([0x11, 0x11, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8])

velocities = [0x11, 0x11] + rpmArrayToHex(motorSpeed)
print(velocities)
velocities = bytes(velocities)



stop = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

kick = bytes([0x11, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14])

# 0xabc = 2748
# 0xf544 = -2748
forwards = bytes([0x11, 0x11, 0xf5, 0x44, 0xf5, 0x44, 0x0a, 0xbc, 0x0a, 0xbc, 0x14])
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

#visuals = Plotter()
t=0


def moveCommands():
    control = input("Enter move command. WASD, QE, K, or nothing to stop\n").upper()
    if (control == "K"):
        sendToEmbedded(kick)
    elif (control == "W"):
        for i in range(100):
            sendToEmbedded(forwards)
            print(f"Sent {forwards}")
            print(f"Received {readFromEmbedded}")
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
        if (len(sys.argv) == 1):
            moveCommands()
        
        elif (len(sys.argv) > 1 and sys.argv[1] == "-a"):
            velocities = [0x11, 0x11] + rpmArrayToHex(motorSpeed)
            velocities = bytes(velocities)

            sendToEmbedded(velocities)
            print(f"Sent: {velocities}")

            actual_b = readFromEmbedded()
            print(actual_b)
            if str(actual_b) == "None":
                print("NOTHING RECEIVED")
                continue
            
            # visuals = Plotter()
            expectedRpmArray = hexToRpmArray(16, binascii.hexlify(velocities).decode()) #[motorSpeed, motorSpeed, motorSpeed, motorSpeed])
            actualRpmArray = hexToRpmArray(8, actual_b) 
            

            
            pidValues = []
            motorSpeed[0] = (pid1.pid_calc(actualRpmArray[0]))
            #print(f"Wheel 1 PID output: {pidValues[0]}")
            motorSpeed[1] = (pid2.pid_calc(actualRpmArray[1]))
            #print(f"Wheel 2 PID output: {pidValues[1]}")
            motorSpeed[2] = (pid3.pid_calc(actualRpmArray[2]))
            #print(f"Wheel 3 PID output: {pidValues[2]}")
            motorSpeed[3] = (pid4.pid_calc(actualRpmArray[3]))
            #print(f"Wheel 4 PID output: {pidValues[3]}")
            
            print(f"Expected: {expectedRpmArray}")
            
            print(f"Actual: {actualRpmArray}")
            visuals.update_plot(t, expectedRpmArray, actualRpmArray)
            
            # velocities = bytes([0x11, 0x11] + rpmArrayToHex(pidValues))
            print(f"New motor speeds: {motorSpeed}")
            if t%35 == 0:
                print("Set new PID values:\n")
                print("Set new PID values:\n")
                Kp = (input("New kP (Press enter to skip): "))

                if (Kp != ""):
                    Kp = int(Kp)
                    Ki = int(input("New kI: "))
                    Kd = int(input("New kD: "))
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
