from ast import Str
from distutils.text_file import TextFile
from http import server
from io import BufferedWriter, TextIOWrapper
from client import genericRequestBuilder
from headerEnums import MessageType
from packet_class import Packet, packetBuilder, objToPacket
from methods import calcPacketSize, multiPacketHandle, messageBuilder, multiSendPacket, fileReadIn, readFilesList
from checkSumMethods import calcChecksum, buildPacketChecksum, checkChecksum
from constants import bf_Size, hr_Size

import socket
import os
import copy

bufferSize = bf_Size
headerSize = hr_Size
serverSocket:socket.socket
txtfiles:str

def serverStart(hostAddress):
    global bufferSize
    global headerSize
    global serverSocket
    global txtfiles

    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n")

    txtfiles = fileReadIn()
    print("server done")
    # -------------------------------------------------------

    while True:
        # ? Handler will always be listening for client requests and responding appropriately
        handler() 

def handler():
    packet:Packet = packetBuilder( serverSocket.recvfrom(bufferSize))

    if (checkChecksum(packet)):
        if (packet.type == 1):
            if (packet.fileIndex == 0):
                printFilesList(packet)

            elif (packet.fileIndex > 0):
                fileRequest(packet)
        else:
            print("!![SERVER]!! ERROR UNKNOWN HEADER TYPE!!!")
    else:
        print("!![SERVER]!! REQUEST CHECKSUM AND CALCULATED CHECKSUM DO NOT MATCH")
        print("!![SERVER]!! PACKET CHECKSUM - ", packet.checkSum)
        print("!![SERVER]!! CALCU  CHECKSUM - ", calcChecksum(buildPacketChecksum(packet)))
        

def fileRequest(packet: Packet):

    filesList:list = readFilesList()
    packetList:list[Packet] = []
    dataSize = bufferSize - headerSize
    file = filesList[packet.fileIndex-1]
    
    #? This could be made into a method or try to support caching in the future?
    for x in range (calcPacketSize(file)):
        start = x * dataSize
        end   = (x+1)*dataSize
        if ( end > len(file)):
            end = end-(end-len(file))
        splitMsg = file[start:end]
        splitMsg = str(splitMsg).encode('utf-8')
    
        packetToSend = copy.copy(packet)
        packetToSend.lastSliceIndex = calcPacketSize(file)
        packetToSend.packetData = splitMsg
        packetList.append(packetToSend) 


    requestedSlice = packetList[packet.sliceIndex-1]
    requestedSlice.sliceIndex = packet.sliceIndex
    requestedSlice.checkSum = calcChecksum(buildPacketChecksum(requestedSlice))
    serverSocket.sendto(objToPacket(requestedSlice), requestedSlice.address)


def printFilesList(packet: Packet): 
    #! this will send an edge case where characters are more than buffer size!!! ERROR!
    multiSendPacket(Packet(MessageType.RES, calcPacketSize(txtfiles), str(txtfiles).encode('utf-8'), packet.ip, packet.port), serverSocket)

