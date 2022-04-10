import socket

buffersize = 32     # total buffer size
header = 6          # total size allocated to header

def serverStart(hostAddress):

    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]
    fullAddress = (hostIP, hostPort)
    # connectedAddress
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    print("\nUDP Server up! \nServerIP: "+str(hostIP)+"\nServerPort: "+str(hostPort)+"\n")


    # -------------------------------------------------------
    while True:
        initialHandshake = serverSocket.recvfrom(buffersize)



def initialHandshakeServer(handshakePacket: bytes):
        connectedHandshakePacket = handshakePacket[0]
        connectedClient = handshakePacket[1]
