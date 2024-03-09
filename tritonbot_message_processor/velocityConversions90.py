import math

def getByteArray(heading, absV, theta, rotV):
    """
    This function takes in four parameters related to heading, absolute
    velocity, theta, and rotational velocity, and returns a byte array.
    
    :param heading: Direction the robot is facing
    :param absV: Absolute velocity of the object
    :param theta: Theta is the angle of rotation in degrees
    :param rotV: Rotational velocity
    """
     twoPI = 2*math.pi
     maxRPM = 3000
	 # insert real wheel radius here
     r = 0.05

	 # insert real wheel distance-to-center here
     d = 0.09

     # the theta we want to go relative to our current heading
     relativeTheta = (theta - heading + 2*twoPI)%twoPI

     # local velocities forward (vx) and left (vy)
     vx = absV * math.cos(relativeTheta)
     vy = absV * math.sin(relativeTheta)

     # angles of wheel relative to the x-axis
     B = [-math.pi/4, math.pi/4, 3*math.pi/4, 5*math.pi/4]

     # position of wheel relative to center
     y = [d* math.cos(math.pi/4),
          d* math.cos(math.pi/4),
          d*-math.cos(math.pi/4),
          d*-math.cos(math.pi/4)]
     x = [d* math.sin(math.pi/4),
          d*-math.sin(math.pi/4),
          d*-math.sin(math.pi/4),
          d* math.sin(math.pi/4)] 

     # set wheel velocities based on desired angle
     M = []
     for i in range(4):
         # apply formula
         M.append((vx-rotV*y[i])*math.cos(B[i]) + (vy+rotV*x[i])*math.sin(B[i]))
         
         # convert from m/s to RPM
         M[i] /= r / 60

     # rescale so that no wheel velocity exceeds our max RPM
     rescale = 1
     for i in range(4):
         rescale = max(rescale, abs(M[i]) / maxRPM)

     for i in range(4):
         M[i] /= rescale
         M[i] = int(M[i])

     # add header
     #send = [0x11]
     send = []

     # add two bytes of info for each motor RPM
     for i in range(4):
         send.append(M[i]>>8 & 0xff)
         send.append(M[i]>>0 & 0xff)
    
     return bytes(send)
