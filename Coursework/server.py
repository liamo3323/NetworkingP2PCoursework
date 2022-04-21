from ast import Str
from http import server
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize, multiPacketHandle, messageBuilder, multiSendPacket
from constants import bf_Size, hr_Size

import socket
import time
import os

global bufferSize
global headerSize
bufferSize = bf_Size
headerSize = hr_Size


def serverStart(hostAddress):

    global serverSocket
    global hostIP
    global hostPort
    global clientConnections

    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    # Keeping track of each connected client
    clientConnections = {}
    # hashmaps- clientConnections[ packet.address ] = packet 
    #? array should keep track of each connections packet request 

    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n")
    
    time.sleep(1)    
    print("Loading...")
    time.sleep(1)
    fileReadIn()
    print("done")
    # -------------------------------------------------------

    while True:
        #? instead of waiting for an initialHandshake at the start a method that handles requests should be written
        initialHandshakeServer()
        handler()

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
 
    replyPacket:Packet = packet[0]
    replyBufferVal = Packet(MessageType.HND, replyPacket.currentPacket, calcPacketSize(bufferSize - headerSize, bufferSize) , replyPacket.checkSum, replyPacket.headCheckSum, replyPacket.req, str(bufferSize).encode('utf-8'), replyPacket.ip, replyPacket.port)
    multiSendPacket(replyBufferVal, serverSocket, bufferSize)

def handler():
    packet = packetBuilder( serverSocket.recvfrom(bufferSize))
    addToConnection(packet)

    if (packet.type == 1): #-request
        print()
    else:
        print("!!ERROR UNKNOWN HEADER REQUEST TYPE!!")

def checkForExistance(packet: Packet) -> bool:
    #checks if incoming packet exists in already established connections

    for x in clientConnections:
        if (x == packet.address):
            return True
    return False

def addToConnection(packet: Packet):
    global clientConnections

    if checkForExistance(packet) is False:
        clientConnections[ packet.address ] = packet
    else:
        print("!!PACKET EXISTS!!")
    
def fileReadIn():
    global txtfiles
    global files
    txtfiles = ""
    files = os.listdir('./resources') # <- this is now a list of files
    for x in files:
        txtfiles = x + ", " + txtfiles
    txtfiles = "["+ txtfiles +"]" + "\nWhich text file would you like to see?"

def returnFileStr(fileInt: int) -> str:
    reqFileName = files[fileInt-1]
    fileLocation = "./resources/"+reqFileName
    file = open(fileLocation, "r")
    return file.read()
