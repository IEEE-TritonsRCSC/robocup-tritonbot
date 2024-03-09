"""Recieve and Send data to embedded design.

This class sends and receives data to and from the STM32 on the robot using
UART. This class assumes a baud rate of 115200 and times out after 1 second
if no data is sent/received. Current convention assumes that the headerbyte of
data received is equal to 0x010101 to avoid receiving garbage data.
"""


import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)


# Initialized message var used for testing
message1 = bytes([0x01, 0x0a, 0xbc, 0x02, 0xbc, 0x02, 0xbc, 0x02, 0xbc])
message2 = bytes([0x11, 0x11, 0x0a, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
stop = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])





def sendToEmbedded(message):
    """Sends the passed message to the robot.

	Takes a message parameter of an array of bytes and sends this to embeddedd
    design via UART.

    Args:
		message:
			The message to be sent to the robot. Although not enforced,
			convention assumes that this is an array of bytes.
	
	Returns: 
		True
    """    
    ser.write(message)
    ser.flush()
    return True


def readFromEmbedded():
    """Receives a message from the robot
    """
    header_byte = ser.read(4)

    if header_byte == b'\x01\x01\x01\x01':
        data = header_byte
        # Read the remaining 8 bytes
        data = ser.read(8)

        # Check if any data was received
        if data:
            # Concatenate the header byte and data
            rx_data = header_byte + data

            # print("RECEIVED: ", rx_data.hex())  # Print hexadecimal representation

        ser.flush()

        return rx_data.hex()
    return


def test():
    """Function to test sending and receiving data
    
    Sends a messaeg to embedded design and waits for a response. Then prints
    the received response. Repeats in a while loop until terminated
    """
    try: 
        while True:
            sendToEmbedded(message2)
            print("sent")
            print(f"Received data: {readFromEmbedded()}")
		
    except KeyboardInterrupt:
        print("\nProgram terminated.")

    finally:
        sendToEmbedded(stop)
        ser.close()


if __name__ == "__main__":
    test()
