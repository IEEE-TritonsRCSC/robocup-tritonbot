from time import sleep
import sys
import yaml
import socket
import select
import ssl_simulation_robot_control_pb2 as RobotControl
import triton_bot_communication_pb2 as Communication
import math
from tritonbot_message_processor.velocityConversions30 import * 
from interface.ai_interface import *
from interface.embedded_systems_interface import *
from analytics.plotter import *

t = 0

# Set the IP address and port to the values defined in config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
server_address = config["serverAddress"]
server_port = config["tritonBotPort"] 

# Create a UDP socket
udp_socket = init_socket(server_address, server_port)

print(f"UDP Server listening on {server_address}:{server_port}")
received_robot_control = Communication.TritonBotMessage()
dribbler_flag = False

"""Main feedback loop

First receives data from AI using the UDP socket and prints feedback that it received
the data. Then, parses the data using protobuf and extracts the wanted values (i.e.
robot local velocity and heading). 
"""
try:
    while True:
        # Receive data from the client
        data, client_address = udp_socket.recvfrom(1024)  # Adjust the buffer size as needed

        # Process the received data (replace this with logic to read the protot file RobotCommand data)
        print(f"Received raw data from {client_address}: {data}")

        received_robot_control.ParseFromString(data)

        actions = received_robot_control.command

        # Print the raw fields and value
        print("Fields and Values:")
        for field_descriptor, value in received_robot_control.ListFields():
            print(f"{field_descriptor.name}: {value}")
            #socket.flush(data)
        
        msg = action_to_byte_array(actions) 
        
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
        header = bytes([0x11]) + bytes([0x11]) # Set header byte
        msg = header + msg + dribbler + kick
              
 
	    # For debugging purposes
        hex_values = [hex(value) for value in msg] # converting binary to hex for ease of reading
        print(msg)
        print(hex_values)

	    # Send data to embedded
        print(sendToEmbedded(msg))	
        actual_b = print(readFromEmbedded())
        
        # Draw up data analytics if -a flag is passed in the command-line args
        if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
            visuals = Plotter()
            expectedRpmArray = getWheelVelocities(actions)
            actualRpmArray = hexToRpmArray(4, actual_b) 
            print(f"Expected: {expectedRpmArray}")
            print(f"Actual: {actualRpmArray}")
            visuals.update_plot(t, expectedRpmArray, actualRpmArray)
        t += 1	
            
        empty_socket(udp_socket)

except KeyboardInterrupt:
    print("Server stopped by user.")
    
    if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
        save = input("Graph plotted. Save to png? (Y/n)\n").upper()
        if save == 'Y':
            saveName = input("What would you like to name this file?\n")
            visuals.save(saveName)


finally:
    # Close the socket when done
    udp_socket.close()
