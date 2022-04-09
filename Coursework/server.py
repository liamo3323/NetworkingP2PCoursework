import socket
from main import BUFFERSIZE, HEAD

def server(hostAddress):

    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]
    fullAddress = (hostIP, hostPort)
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    print("\nUDP Server up! \nServerIP: "+str(hostIP)+"\nServerPort: "+str(hostPort)+"\n")


    # -------------------------------------------------------
    while True:
        connectedClient = serverSocket.recvfrom(BUFFERSIZE)