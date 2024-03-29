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
