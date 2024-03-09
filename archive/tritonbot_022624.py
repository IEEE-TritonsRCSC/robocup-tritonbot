from time import sleep
import socket
import select
import ssl_simulation_robot_control_pb2 as RobotControl
import triton_bot_communication_pb2 as Communication
import math
from embedded_systems_interface import *
from velocityConversions30 import * # Un-comment line below for 90 degree chasis
# from velocityConversions import * 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

expected = []	# Expected wheel velocities (msg's we send to embedded)
actual = []	# Actual wheel velocities
it = 0
def empty_socket(sock):
    """remove the data present on the socket"""
    input = [sock]
    while 1:
        inputready, o, e = select.select(input,[],[], 0.0)
        if len(inputready)==0: break
        for s in inputready: s.recv(1)

# Set the IP address and port to the values you are using in UDP_Client
server_address = "0.0.0.0"  # Use 0.0.0.0 to bind to all available interfaces
server_port = 10500  # Use the port you have configured in UDP_Client. Currently set to team blue bot 0

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
udp_socket.bind((server_address, server_port))

print(f"UDP Server listening on {server_address}:{server_port}")
received_robot_control = Communication.TritonBotMessage()
dribbler_flag = False

try:
    while True:
        # Receive data from the client
        data, client_address = udp_socket.recvfrom(1024)  # Adjust the buffer size as needed

        # Process the received data (replace this with logic to read the protot file RobotCommand data)
        print(f"Received raw data from {client_address}: {data}")

        received_robot_control.ParseFromString(data)

        actions = received_robot_control.command
        local_velocity = received_robot_control.command.move_command.local_velocity
        absV = math.sqrt(local_velocity.forward*local_velocity.forward+local_velocity.left*local_velocity.left)
        theta = math.atan2(local_velocity.left, local_velocity.forward)
        print(absV, theta)

        # Print the raw fields and value
        print("Fields and Values:")
        for field_descriptor, value in received_robot_control.ListFields():
            print(f"{field_descriptor.name}: {value}")
            #socket.flush(data)
		
	# Wheel velocity conversions
        rotV = local_velocity.angular	
        msg = getByteArray(0, absV, theta, rotV)
        
	# Get kick speed as boolean value
        if actions.kick_speed != 0:
            kick = bytes([0x14]) # Set action to kick (kick = true)
        else:
            kick = bytes([0x00])

	# Set dribbler byte to dribbler status
        if actions.dribbler_speed == 0 and dribbler_flag == True:
            dribbler = bytes([0x13]) # Turn off dribbler
            dribbler_flag = False
        elif actions.dribbler_speed > 0 and dribbler_flag == False:
            dribbler = bytes([0x12]) # Turn on dribbler
            dribbler_flag = True
        else:
            dribbler = bytes([0x00]) # Do nothing (Activate motors) 
 
        # Create header and assemble msg
        header = bytes([0x11]) # Set header byte
        msg = header + msg + dribbler + kick
              
 
	# For debugging purposes
        hex_values = [hex(value) for value in msg] # converting binary to hex for ease of reading
        print(msg)
        print(hex_values)

	# Send data to embedded
        print(sendToEmbedded(msg))	
        print(readFromEmbedded())

	# Keep track of data
	expected.append(msg)
	actual.append(readFromEmbedded())

	# Plot data after 20 iterations
	if(it == 20):
		plotter(20, actual, expected)
		actual = []
		expected = []
		it++	# Only do 1 plot of 20 iterations for now
	it++	
		
        empty_socket(udp_socket)

except KeyboardInterrupt:
    print("Server stopped by user.")

finally:
    # Close the socket when done
    udp_socket.close()

'''
def animate(it, rawActual, expected):
	data_as_list = rawActual.split(b',')
	
	data_as_list = data_as_list[1]
	# I dont know how read data looks yet but thats how splitting works i think

	xs.append(it)	
	actual_header_byte = data_as_list[0]
	actual_w0_bytes = int(data_as_list[1] + data_as_list[2])
	actual_w1_bytes = int(data_as_list[3] + data_as_list[4])
	actual_w2_bytes = int(data_as_list[5] + data_as_list[6])
	actual_w3_bytes = int(data_as_list[7] + data_as_list[8])

	actualHeader.append(actual_header_byte)
	actualW0.append(actual_w0_bytes)
	actualW1.append(actual_w1_bytes)
	actualW2.append(actual_w2_bytes)
	actualW3.append(actual_w3_bytes)	

	expHeader.append(exp_header_byte)
	expW0.append(exp_w0_bytes)
	expW1.append(exp_w1_bytes)
	expW2.append(exp_w2_bytes)
	expW3.append(exp_w3_bytes)

	# Only plotting wheel 0 speed for now
	ax.clear()
	ax.plot(xs, actual_w0_bytes, label="Actual Wheel 0 Speed")
	ax.plot(xs, exp_w0_bytes, label="Expected Wheel 0 Speed")
	
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.ylabel('Speeds')
	plt.axis([1, None, 0, 1.1])
'''
