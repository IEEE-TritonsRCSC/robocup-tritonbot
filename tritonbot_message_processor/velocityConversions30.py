import math
import ssl_simulation_robot_control_pb2 as RobotControl
import triton_bot_communication_pb2 as Communication

def getByteArray(heading, absV, theta, rotV):
    """
    This function takes in heading, absolute velocity, theta, and rotational
    velocity as input parameters and returns a byte array.
    
    :param heading: Heading is the direction in which an object is pointing, usually
    measured in degrees. It indicates the angle between the object's orientation and
    a reference direction, often the north direction
    :param absV: Absolute velocity of the object
    :param theta: Theta is the angle of rotation in degrees
    :param rotV: The `rotV` parameter seems to be missing its description. Could you
    please provide more information on what `rotV` represents or what it is used for
    in the `getByteArray` function?
    """
    twoPI = 2*math.pi
    maxRPM = 15000

    # constants
    relativeTheta = (theta - heading + 2*twoPI)%twoPI
    vx = absV*math.cos(relativeTheta)
    vy = absV*math.sin(relativeTheta)
    d = 0.13
    r = 0.05

    # angle of wheel relative to the x-axis
    B = [-math.pi/6,math.pi/6,5*math.pi/6,7*math.pi/6]

    # position of wheel relative to center
    y = [d*math.cos(math.pi/6),d*math.cos(math.pi/6),d*-math.cos(math.pi/6),d*-math.cos(math.pi/6)]
    x = [d*math.sin(math.pi/6),d*-math.sin(math.pi/6),d*-math.sin(math.pi/6),d*math.sin(math.pi/6)]
 
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
    #send = [0x0]
    send = []

    # add two bytes of info from each motor RPM
    for i in range(4):
        send.append(M[i]>>8 & 0xff)
        send.append(M[i]>>0 & 0xff)
        print(M[i])

    #send[2] = 0xab
    #send[3] = 0x11
    return bytes(send)

def action_to_byte_array(action):
    """
    This function converts an action into a byte array.
    
    :param action: kick/dribble/etc
    TODO
    """
    loc_v = action.move_command.local_velocity
    absV = math.sqrt(loc_v.forward*loc_v.forward + loc_v.left*loc_v.left)
    theta = math.atan2(loc_v.left, loc_v.forward)
    rotV = loc_v.angular

    return getByteArray(0, absV, theta, rotV)
