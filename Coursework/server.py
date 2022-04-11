import socket
from headerEnums import MessageType
from packet_class import packet
from methods import calcPacketSize
from constants import bf_Size, hr_Size
bufferSize = bf_Size
headerSize = hr_Size

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
        initialHandshakeServer(serverSocket)
        

def initialHandshakeServer(socket: socket.socket):
    
    global bufferSize, headerSize

    initialHandshake = socket.recvfrom(bufferSize)
    connectedHandshakePacket = initialHandshake[0]
    connectedHandshakeAddress = initialHandshake[1]
    bufferSizeRecieve = connectedHandshakePacket.decode()
    recievedValue = int(bufferSizeRecieve[6:])

    if (recievedValue > bufferSize):
        bufferSize = recievedValue

    print("The BIGGEST buffer ", bufferSize)      
    
    packetDataSize = bufferSize - headerSize
    replyBufferVal = packet(MessageType.hnd, calcPacketSize(packetDataSize, bufferSize) , bufferSize.to_bytes(, 'little'), connectedHandshakeAddress[0], connectedHandshakeAddress[1])
    print(bufferSize)
    print(replyBufferVal.packetData)
    socket.sendto(replyBufferVal.packet, replyBufferVal.address)