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

	Args:
		address:
			The IP address that we want the socket to bind to
		port:
			The port on the IP address we want the socket to bind to

	Returns:
		The newly created socket
	"""

    # create a UDP socket
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to the input address and port
	udp_socket.bind((address, port))

    # return the upd socket
	return udp_socket
