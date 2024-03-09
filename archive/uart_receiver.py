import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', baudrate=115200)

def read_from_uart():
    while True:
        # Read 1 byte
        header_byte = ser.read(4)
        
        if header_byte == b'\x01\x01\x01\x01':
            data = header_byte
            # Read the remaining 8 bytes
            data = ser.read(8)

            # Check if any data was received
            if data:
                # Concatenate the header byte and data
                rx_data = header_byte + data

                print("Received data:", rx_data.hex())  # Print hexadecimal representation

        # Add a small delay to avoid high CPU usage in the loop
        ser.flush()
        sleep(0.1)

try:
    read_from_uart()
except KeyboardInterrupt:
    # Handle Ctrl+C to gracefully exit the program
    print("\nProgram terminated.")
finally:
    # Close the serial port when done
    ser.close()






'''
import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', baudrate=115200)

def read_from_uart():
    while True:
        # Read 33 bytes
        rx_data = ser.read()
        i = 0

        #print(rx_data)
        
        if (1):
            data = ser.read()	
            if (data == 0x01):
                while i < 8:				
                    rx_data += data
                    i += 1
                    # print("i incremented")
        
            # rx_data = ser.read(33)
        
        		# Check if any data was received
                if rx_data and rx_data != 0:
                    print("Received data:", rx_data)
        #rx_data.flush()
        ser.flush()
        # Add a small delay to avoid high CPU usage in the loop
        sleep(0.1)

try:
    read_from_uart()
except KeyboardInterrupt:
    # Handle Ctrl+C to gracefully exit the program
    print("\nProgram terminated.")
finally:
    # Close the serial port when done
    ser.close()

'''









'''
import serial
import time

# Define the UART port and baud rate
uart_port = "/dev/ttyS0"  
baud_rate = 11520

# Create a serial connection
ser = serial.Serial(uart_port, baud_rate, timeout=1)

# Function to receive data over UART
def receive_data():
    # Read data from the UART port
    data_bytes = ser.readline()

    return data_bytes.strip()





# Receive data and print it
while (1):
	received_data = receive_data()
	print(f"Received data: {received_data}")

# Close the serial connection when done
ser.close()
'''
