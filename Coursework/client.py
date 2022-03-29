import socket

#OLD ORIGINAL
def startClient():
    msgFromClient       = "Hello UDP Server this is the Client"
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = ("127.0.0.1", 20001) #im going to guess that 127.0.0.1 is local host and 20001 is the port 
    bufferSize          = 1024 #temp buffer size for now 

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    #UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    UDPClientSocket.connect(serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)