import math
import ssl_simulation_robot_control_pb2 as RobotControl
import triton_bot_communication_pb2 as Communication

def getVelocityArray(heading, absV, theta, rotV):
    """
    The `getVelocityArray` function takes heading, absolute velocity, theta, and
    rotational velocity as input parameters and returns a byte array.
    
    :param heading: Heading is the direction in which an object is pointing, usually
    measured in degrees. It indicates the angle between the object's orientation and
    a reference direction, often the north direction
    :param absV: Absolute velocity is the speed of an object in a given direction,
    regardless of its direction of motion. It is a scalar quantity and is typically
    measured in units such as meters per second (m/s) or kilometers per hour (km/h)
    :param theta: Theta is the angle of rotation in degrees. It represents the
    amount of rotation or angular displacement of an object from its reference
    position. In the context of the `getVelocityArray` function, the `theta`
    parameter likely influences the calculation of the byte array based on the
    rotation angle provided
    :param rotV: RotV represents the rotational velocity of the object. It indicates
    the rate at which the object is rotating around its axis. This parameter is used
    in the `getVelocityArray` function to calculate and include the rotational
    velocity information in the byte array that is returned by the function
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
    
    return M

def valuesToBytes(M):
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

def getWheelVelocities(action):
    """
    The function `getWheelVelocities` calculates the velocity components for a given
    action and returns them as a byte array.
    
    :param action: The `action` parameter is an object that contains a
    `move_command` attribute, which in turn has a `local_velocity` attribute. This
    `local_velocity` attribute contains information about the velocity of the robot
    in different directions: `forward`, `left`, and `angular`
    :return: the result of calling the `getVelocityArray` function with arguments 0,
    `absV`, `theta`, and `rotV`.
    """
    loc_v = action.move_command.local_velocity
    absV = math.sqrt(loc_v.forward*loc_v.forward + loc_v.left*loc_v.left)
    theta = math.atan2(loc_v.left, loc_v.forward)
    rotV = loc_v.angular

    return getVelocityArray(0, absV, theta, rotV)

def action_to_byte_array(action):
    return valuesToBytes(getWheelVelocities(action))




# This function is used purely for data analytic purposes
def hexToRpmArray(headerLength, data):
    """
    This function converts a hexadecimal string to an array of RPM values.
    
    :param headerLength: The `headerLength` parameter specifies the length of the
    header in the data array. This information is important for parsing the data
    correctly
    :param data: data to convert from hex to rpm
    TODO
    """
    pass