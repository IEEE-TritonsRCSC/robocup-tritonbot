import math
import proto.ssl_simulation_robot_control_pb2 as RobotControl
import proto.triton_bot_communication_pb2 as Communication

def getVelocityArray(heading, absV, theta, rotV):
    """
    The `getVelocityArray` function takes heading, absolute velocity, theta, and
    rotational velocity as input parameters and returns a byte array.
    
    :param heading: Heading is the direction the robot is pointing in relative to the
	"upwards" direction (in terms of the global field orientation) as of this moment.
    :param absV: The desired absolute translational speed of the robot, in meters per second.
    :param theta: The desired direction the robot should move in, relative to the "upwards"
	direction. Measured in radians. For example, theta = pi/2 means we want to move west,
	while theta = -pi/4 means we want to move north-east
    :param rotV: The desired rotational velocity of the robot, in radians per second.

    :return: An integer array containing the desired speeds (in RPM) of each wheel
    """
    twoPI = 2*math.pi
    maxRPM = 15000

    # constants
    relativeTheta = (theta - heading + 2*twoPI)%twoPI
    vx = absV*math.cos(relativeTheta)
    vy = absV*math.sin(relativeTheta)
    d = 0.13
    r = 0.045

    # angle of each wheel relative to the x-axis
    B = [-math.pi/6,math.pi/6,5*math.pi/6,7*math.pi/6]

    # position of each wheel relative to center
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
    """ 
    Converts an integer array into a byte array with each integer split into 
    its first two bytes    
    """

    # initialize array
    send = []

    # add two bytes of info from each motor RPM
    for i in range(4):
        send.append(M[i]>>8 & 0xff)
        send.append(M[i]>>0 & 0xff)
        print(M[i])

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
    """ 
    Effectively an overload of getWheelVelocities that returns the desired wheel 
    velocities split into two bytes each in a way that embedded can read
    """
    return valuesToBytes(getWheelVelocities(action))

# This function is used purely for data analytic purposes
def hexToRpmArray(headerLength, data):
    """
    This function converts a hexadecimal string to an array of integer RPM values.
    
    :param headerLength: The `headerLength` parameter specifies the length of the
    header in the data array. This information is important for parsing the data
    correctly
    :param data: string data to convert from hex to rpm
    """
    rpm = []
    
    for i in range(4):
        hexSpeed = int(data[headerLength + 4*i : headerLength + 4*i + 4], 16)
        speed = -(hexSpeed & 0x8000) | (hexSpeed & 0x7fff)
        rpm.append(int(str(speed), 10))
        
    return rpm

# This function is used purely for data analytic purposes
def rpmArrayToHex(motorSpeed):
    """
    This function converts an array of RPM values to a binary string representing hexadecimal values.
    
    :param motorSpeed: An array of integer RPM values to convert to hexadecimal. eg: [200, 240, 232, 249]
    :return: A binary string representing hexadecimal values.
    """

    velocities = []
    for speed in motorSpeed:
        velocities.append((speed>>8) & 0xff)
        velocities.append(speed & 0xff)
    
    return velocities
