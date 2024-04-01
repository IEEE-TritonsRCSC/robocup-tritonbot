"""Receive data from AI.

This class initializes and uses a socket to communicate with the AI simulation.
"""

import socket
import select

def empty_socket(sock):
	"""Function to read data from socket (AI)

	Continues to clear the input buffer until there is no more data to receive.
	"""

	input = [sock]
	while 1:
		inputready, o, e = select.select(input, [], [], 0.0)
		if len(inputready) == 0: break
		for s in inputready: s.recv(1)

def init_socket(address, port):
	"""Initializes a socket connection with AI

	Creates a socket that binds the given address and port.

	:param address: The IP address that we want the socket to bind to
	:param port: The port on the IP address we want the socket to bind to

	:return: The newly created socket
	"""

    	# create a UDP socket
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
    	# bind the socket to the input address and port
	udp_socket.bind((address, port))

	# join multicast
	udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
			      socket.inet_aton(address) + socket.inet_aton('0.0.0.0'))

    	# return the upd socket
	return udp_socket
