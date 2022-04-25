from email.mime import multipart
import socket
import time
import re
from typing import Tuple
from xmlrpc.client import Boolean
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
    clientSocket.settimeout(5)    

    time.sleep(2)
    print("\nUDP client up connecting to!\nClientIP: ",str(targetIP),"\nclientPort: ",str(targetPort),"\nBuffer Size: ", str(bufferSize),"\n")
    print("client done")

    # -------------------------------------------------------
    while True:
        clientRequest = genericRequestBuilder(input())
        multiSendPacket (clientRequest, clientSocket, bufferSize)
        print(messageBuilder(multiPacketHandle(clientSocket, bufferSize, clientRequest)))

def genericRequestBuilder(clientInput:str) ->Packet:
    if (clientInput == "givelist"):
        return Packet(MessageType.GIV, 1, calcPacketSize(bufferSize - headerSize, headerSize), 0, 0, 0, bytes(), targetIP, targetPort)
    elif (re.search("^req", clientInput)):
        print("Success")
        number = listToInt(re.findall("\d", clientInput))
        return Packet(MessageType.REQ, 1, calcPacketSize(bufferSize - headerSize, headerSize), 0, 0, number, bytes(), targetIP, targetPort)
    else:
        print("!!!ERROR INVALID REQUEST!!!")

def listToInt(list:list)->int:
    total:str = ""
    for x in list:
        total = total + x
    return int(total)
