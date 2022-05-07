from email.message import Message
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
    clientSocket.settimeout(10) # timeout of 5 is set to allow for request to be sent again when timeout is reached

    # sleep timer is to prevent client loaded and server loaded message to have runtime issue both printing at the same time over each other
    time.sleep(0.1)
    print("\nUDP client up connecting to!\nClientIP: ",str(targetIP),"\nclientPort: ",str(targetPort),"\nBuffer Size: ", str(bufferSize),"\n\n Client done!\n")

    # Once the client has loaded, it makes a request to the server for the 0th index as stated in the RFC
    clientRequest = Packet(MessageType.REQ, calcPacketSize(headerSize), bytes(), targetIP, targetPort)
    multiSendPacket (clientRequest, clientSocket )
    print( buildIndexZero(messageBuilder(multiPacketHandle(clientSocket, clientRequest))))
    # -------------------------------------------------------------------------------------------------------------------------
    while True:
        # Requests are made dependent on what user input is
        clientRequest = genericRequestBuilder()                      # generticRequestBuilder makes a generic request for a file using user input
        print("\n[Client] ---loading---\n")
        multiSendPacket (clientRequest, clientSocket )                      # multiSendPacket splits packets up into slices and sends them off to an address
        serverResponse = multiPacketHandle(clientSocket, clientRequest)     # client then listens for packet resposne from server and loads into serverResponse
        builtMessage = messageBuilder(serverResponse)                       # the serverResponse fully build packet is then read into messageBuilder to concatonate the decoded UTF-8  slices into a singular message
        if (serverResponse[0].fileIndex == 0):
            builtMessage = buildIndexZero(builtMessage)                     # However, if the packet returned is a list of all files connected PEER has, it will maniulate the string and make it more readable for users
        print(builtMessage)                                                 # this is possible because a specific format the 0th file index will be sent in has been written on the RFC

def genericRequestBuilder() ->Packet:                        # helper method which will return different requests depending on user input
    clientInput = input()
    if (clientInput == "givelist"):
        return Packet(MessageType.REQ, calcPacketSize(headerSize), bytes(), targetIP, targetPort)
    
    elif (re.search("^req", clientInput.lower())):
        number = listToInt(re.findall("\d", clientInput))
        fileRequestPac = Packet(MessageType.REQ, calcPacketSize(headerSize), bytes(), targetIP, targetPort, number)
        fileRequestPac.fileIndex = number
        return (fileRequestPac)
    
    else:
        print("!![CLIENT]!! ERROR INVALID REQUEST! PLEASE ENTER A LEGAL REQUEST TYPE!!!")
        return genericRequestBuilder()

