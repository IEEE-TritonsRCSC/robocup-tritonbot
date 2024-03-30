'''
wheelAll = bytes([0x11, 0x11, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8])

#print(str(wheelAll))


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
        print(f"Hex Speed: {hexSpeed}")
        speed = -(hexSpeed & 0x80000000) | (hexSpeed & 0x7fffffff)
        print(f"Speed: {speed}")
        rpm.append(int(str(speed), 10))
        
    return rpm

#print(hexToRpmArray(8, b'0101010185a41554154914e2'))

hexSpeed = int('ffff', 16)  # Corrected the hexadecimal value
speed = -(hexSpeed & 0x8000) | (hexSpeed & 0x7fff)  # Corrected the bit masking
print(speed)



def rpmArrayToHex(rpm):
    """
    This function converts an array of RPM values to a binary string representing hexadecimal values.
    
    :param rpm: An array of integer RPM values to convert to hexadecimal.
    :return: A binary string representing hexadecimal values.
    """
    hex_string = b""
    
    for speed in rpm:
        # Convert RPM to hexadecimal string
        hex_speed = format(speed & 0xFFFF, '04x')  # Ensure 4-character width and hexadecimal representation
        
        # Convert hexadecimal string to binary and append to result
        hex_string += str(bytes.fromhex(hex_speed))
    
    return str(hex_string)


# Example usage:
rpm = [1000, -2000, 3000, -4000]
hex_data = rpmArrayToHex(rpm)
print(hex_data)
'''

import binascii

wheelAll = bytes([0x11, 0x11, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8, 0x0b, 0xb8])

# Convert bytes object to hexadecimal string and decode it
hex_string = binascii.hexlify(wheelAll).decode()
#print(hex_string)

motorSpeed = -1 
higherByte = (motorSpeed >> 8) & 0xff
lowerByte = motorSpeed & 0xff

velocities = [0x11, 0x11]
for i in range(4):
    velocities.append(motorSpeed>>8 & 0xff)
    velocities.append(motorSpeed & 0xff)
print(bytes(velocities))
