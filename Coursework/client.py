import socket
import time
from typing import Tuple
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize, multiSendPacket, multiPacketHandle, messageBuilder
from constants import hr_Size, bf_Size
global bufferSize
global headerSize
bufferSize = bf_Size
headerSize = hr_Size

def clientStart(connectionAddress): 

    global clientSocket
    global targetIP
    global targetPort

    # * Address where client wants to connect to
    targetIP     = connectionAddress[0]
    targetPort   = connectionAddress[1]

    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    print("\nUDP client up connecting to!\nClientIP: ",str(targetIP),"\nclientPort: ",str(targetPort),"\nBuffer Size: ", str(bufferSize),"\n")
    
    print("Loading...")
    time.sleep(2)
    print("done")

    initialHandshakeClient() 
    # -------------------------------------------------------
    while True:
        clientInput = input() # string input --> server 

def initialHandshakeClient():
    #* client will send a packet to server and confirm agreed buffer size
    #* and get a responce of the smallest packet between the two and use 
    #* said buffer size for all future data sending

    global bufferSize
    packetInitialHandshake = Packet(MessageType.hnd, 1, calcPacketSize(bufferSize-headerSize, bufferSize) , str(bufferSize).encode('utf-8'), targetIP, targetPort)    
    #multiSendPacket(packetInitialHandshake, clientSocket, bufferSize)
    clientSocket.sendto(packetInitialHandshake.packet, packetInitialHandshake.address)
    
    packets = multiPacketHandle(clientSocket, bufferSize)

    bufferSize = int( messageBuilder(packets) )
    print("The agreed upon buffer size is "+ str(bufferSize))