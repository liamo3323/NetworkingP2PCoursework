from email.mime import multipart
import socket
import time
import re
from typing import Tuple
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize, multiSendPacket, multiPacketHandle, messageBuilder, listToInt, buildIndexZero
from constants import bf_Size, hr_Size



bufferSize = bf_Size
headerSize = hr_Size

# initializing variables and type declaration for type security
clientSocket:socket.socket
targetIP:str
targetPort:int

def clientStart(connectionAddress): 
    # making variables global variables to be called inside other functions
    global bufferSize
    global headerSize

    global clientSocket
    global targetIP
    global targetPort

    # connectionAddress is a touple where index 0 is the IP address the clients connects to and index 1 is the HOST address
    targetIP = connectionAddress[0]
    targetPort = connectionAddress[1]

    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    clientSocket.settimeout(5) # timeout of 5 is set to allow for request to be sent again when timeout is reached

    print("\nUDP client up connecting to!\nClientIP: ",str(targetIP),"\nclientPort: ",str(targetPort),"\nBuffer Size: ", str(bufferSize),"\n\n Client done!")

    # -------------------------------------------------------
    while True:
        clientRequest = genericRequestBuilder(input())
        print("\n---loading---\n")
        multiSendPacket (clientRequest, clientSocket )
        serverResponse = multiPacketHandle(clientSocket, clientRequest)
        builtMessage = messageBuilder(serverResponse)
        if (serverResponse[0].fileIndex == 0):
            builtMessage = buildIndexZero(builtMessage)
        print(builtMessage)

def genericRequestBuilder(clientInput:str) ->Packet:
    if (clientInput == "givelist"):
        return Packet(MessageType.REQ, calcPacketSize(headerSize), bytes(), targetIP, targetPort)
    
    elif (re.search("^req", clientInput)):
        number = listToInt(re.findall("\d", clientInput))
        fileRequestPac = Packet(MessageType.REQ, calcPacketSize(headerSize), bytes(), targetIP, targetPort, number)
        fileRequestPac.fileIndex = number
        return (fileRequestPac)
    
    else:
        print("!![CLIENT]!! ERROR INVALID REQUEST!!!")
        return Packet(MessageType.REQ, 0, bytes(), "", 0)

