import socket
import time
from typing import Tuple
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize
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
    time.sleep(1)
    initialHandshakeClient() 
    # -------------------------------------------------------
    while True:
        print("The agreed upon buffer size is "+ str(bufferSize))
        clientInput = input() # string input --> server 

def initialHandshakeClient():
    #* client will send a packet to server and confirm agreed buffer size
    #* and get a responce of the smallest packet between the two and use 
    #* said buffer size for all future data sending

    global bufferSize
    print(MessageType.hnd).value
    packetInitialHandshake = Packet(MessageType.hnd, 1, calcPacketSize(bufferSize-headerSize, bufferSize) , str(bufferSize).encode('utf-8'), targetIP, targetPort)    
    clientSocket.sendto(packetInitialHandshake.packet, packetInitialHandshake.address)
    initialHandshake = packetBuilder( clientSocket.recvfrom(bufferSize))
    bufferSize = int(initialHandshake.packetData.decode())
    print("The agreed upon buffer size is "+ str(bufferSize))