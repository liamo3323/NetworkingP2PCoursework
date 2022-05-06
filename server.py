from ast import Str
from distutils.text_file import TextFile
from email.message import Message
from http import server
from io import BufferedWriter, TextIOWrapper
from wsgiref import headers
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
    txtfiles = fileReadIn()
    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n\n Server done!\n")



    # -------------------------------------------------------

    while True:
        # ? Handler will always be listening for client requests and responding appropriately
        handler() 

def handler():
    packet:Packet = packetBuilder( serverSocket.recvfrom(bufferSize))
    print("[Server] Packet Recieved! Packet: ", (packet.packet))
    print("[Server] Packet Recieved! Packet size: ", len(objToPacket(packet)))

    if (checkChecksum(packet) and packet.sliceIndex != 0):
        if (packet.type == 1):
            if (packet.fileIndex == 0):
                printFilesList(packet)

            elif (packet.fileIndex > 0 and packet.fileIndex <= len(readFilesList())):
                fileRequest(packet)
            else:
                print("!![SERVER]!! REQUEST FILE INDEX DOES NOT EXIST")
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
    requestedSlice.bodyLength = (len(objToPacket(requestedSlice))-headerSize)   
    print("size of requested packet: ", (len(objToPacket(requestedSlice))-headerSize))
    requestedSlice.type = MessageType.RES.value
    requestedSlice.checkSum = calcChecksum(buildPacketChecksum(requestedSlice))
    print("[Server] Server is repsonding with...",objToPacket(requestedSlice))
    serverSocket.sendto(objToPacket(requestedSlice), requestedSlice.address)


def printFilesList(packet: Packet): 
    packetList:list[Packet] = []
    dataSize = bufferSize - headerSize

    for x in range (calcPacketSize(txtfiles)):
        start = x * dataSize
        end   = (x+1)*dataSize
        if ( end > len(txtfiles)):
            end = end-(end-len(txtfiles))
        splitMsg = txtfiles[start:end]
        splitMsg = str(splitMsg).encode('utf-8')
    
        packetToSend = copy.copy(packet)
        packetToSend.lastSliceIndex = calcPacketSize(txtfiles)
        packetToSend.packetData = splitMsg
        packetList.append(packetToSend) 


    requestedSlice = packetList[packet.sliceIndex-1]
    requestedSlice.sliceIndex = packet.sliceIndex
    requestedSlice.bodyLength = len(objToPacket(requestedSlice))
    requestedSlice.type = MessageType.RES.value  
    requestedSlice.checkSum = calcChecksum(buildPacketChecksum(requestedSlice))
    print("[Server] Server is repsonding with...",objToPacket(requestedSlice))
    serverSocket.sendto(objToPacket(requestedSlice), requestedSlice.address)