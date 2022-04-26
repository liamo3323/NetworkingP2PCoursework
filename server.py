from ast import Str
from distutils.text_file import TextFile
from http import server
from io import BufferedWriter, TextIOWrapper
from client import genericRequestBuilder
from headerEnums import MessageType
from packet_class import Packet, packetBuilder, objToPacket
from methods import calcPacketSize, multiPacketHandle, messageBuilder, multiSendPacket
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

    #! checking if checksum is right
    if (checkChecksum(packet)):

        print(packet.packet)
        if (packet.type == 1): #-request
            if (packet.fileIndex == 0):
                printFilesList(packet)
            elif (packet.fileIndex > 0):
                fileRequest(packet)
        else:
            print("!!ERROR UNKNOWN HEADER REQUEST TYPE!!")
        
def fileReadIn()-> str:
    txtfiles = ""
    files = os.listdir('./resources') # <- this is now a list of files
    ctr = 1
    for x in files:
        fileLocation = "./resources/"+x
        IOwrapperFile = open(fileLocation, "r")
        file = IOwrapperFile.read()
        txtfiles = str(ctr) + ":"+str(len(file))+":"+x + "\n"+txtfiles
        ctr = ctr + 1
    txtfiles = txtfiles + "\nWhich text file would you like to see?"
    return txtfiles

def fileRequest(packet: Packet):
    files = os.listdir('./resources')
    try:
        reqFileName = files[packet.fileIndex-1]
        fileLocation = "./resources/"+reqFileName
        IOwrapperFile = open(fileLocation, "r")
        file = IOwrapperFile.read()
        #multiSendPacket(Packet(MessageType.RES, calcPacketSize(file), str(file).encode('utf-8'), packet.ip, packet.port, packetFileIndex = packet.fileIndex-1,), serverSocket)

    except:
        return ("!!File does not exist!!")
        #? file is a list of files that the computer has read in
        #! I need to then split the files 

        #! Loop below will split the requested file index into the correct data sizes 

    packetList:list[Packet] = []
    dataSize = bufferSize - headerSize
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
    multiSendPacket(Packet(MessageType.RES, calcPacketSize(txtfiles), str(txtfiles).encode('utf-8'), packet.ip, packet.port), serverSocket)

