# UDPPingerClient.py
# We will need the following module to generate randomized lost packets
import sys
import socket
print("server")

# Create a UDP socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000
Message = b"Hello, Server"

# create a socket with a 1s timeout.

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
s.sendall(b"Hello, world")
data = s.recv(1024)

for i in range(0, 10):  # sends 10 pings
	# Send data
	print('sending "%s"' % Message)
	try:
		# sent the Message using the clientSock
		sent = 1024
		# Receive response
		print('waiting to receive')
		# get the response & extract data
		
		print('received "%s"' % data)

	except socket.timeout as inst:
		# handle timeouts
		print('Request timed out')

print ('closing socket')
# close the socket
