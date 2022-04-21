from http import server
import socket
import time
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize, multiPacketHandle, messageBuilder, multiSendPacket
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

    # Keeping track of each connected client
    clientConnections = []

    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n")
    
    time.sleep(1)    
    print("Loading...")
    time.sleep(1)
    print("done")
    # -------------------------------------------------------

    while True:
        #? instead of waiting for an initialHandshake at the start a method that handles requests should be written
        initialHandshakeServer()
        incomingListener()

def initialHandshakeServer(): 
    #* Server will realize that client is sending a handshake packet
    #* and calculate lowest buffer size between client + server and 
    #* reply the smallest buffer between the two
    

    global bufferSize, headerSize
    
    #packet = packetBuilder( serverSocket.recvfrom(bufferSize))
    packet = multiPacketHandle(serverSocket, bufferSize)

    recievedValue = int(messageBuilder(packet))

    if (recievedValue < bufferSize):
        print("| Agreeing on smaller buffer size |")
        bufferSize = recievedValue  
 
    replyBufferVal = Packet(MessageType.HND, calcPacketSize(bufferSize - headerSize, bufferSize) , str(bufferSize).encode('utf-8'), packet[0].ip, packet[0].port)
    multiSendPacket(replyBufferVal, serverSocket, bufferSize)

def incomingListener():
    packet = packetBuilder( serverSocket.recvfrom(bufferSize))
    if (packet.type == 1): #-request
        print()
    else:
        print("!!ERROR UNKNOWN HEADER REQUEST TYPE!!")
