import socket
import time
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize
from constants import bf_Size, hr_Size
global bufferSize
global headerSize
bufferSize = bf_Size
headerSize = hr_Size


def serverStart(hostAddress):

    global serverSocket
    global hostIP
    global hostPort

    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n")
    
    print("Loading...")
    time.sleep(2)
    print("done")
    # -------------------------------------------------------

    while True:
        #? instead of waiting for an initialHandshake at the start a method that handles requests should be written
        incomingListener()
        print("Server- The agreed upon buffer size is "+ str(bufferSize))


def initialHandshakeServer(packet: Packet): 
    #* Server will realize that client is sending a handshake packet
    #* and calculate lowest buffer size between client + server and 
    #* reply the smallest buffer between the two
    print("starting the handshake! ")
    global bufferSize, headerSize
    initialHandshake = packet
    recievedValue = int(packet.packetData.decode())

    if (recievedValue < bufferSize):
        bufferSize = recievedValue  
 
    replyBufferVal = Packet(MessageType.hnd, 1, calcPacketSize(bufferSize - headerSize, bufferSize) , str(bufferSize).encode('utf-8'), initialHandshake.ip, initialHandshake.port)
    print("sending reply handshake")
    serverSocket.sendto(replyBufferVal.packet, replyBufferVal.address)


def incomingListener():
    incomingPacket = packetBuilder(serverSocket.recvfrom(bufferSize))

    if (incomingPacket.type == 1): #-Initial HandShake
        initialHandshakeServer(incomingPacket)
    elif (incomingPacket.type == 2): #-request
        print()
    elif (incomingPacket.type == 3): #-finished data transmission
        print()
    elif (incomingPacket.type == 4): #-give list of files
        print()
    elif (incomingPacket.type == 5): #-request specific docu
        print()
    else:
        print("!!ERROR UNKNOWN HEADER REQUEST TYPE!!")