from ipaddress import ip_address
from logging import exception
from packet_class import Packet, packetBuilder, objToPacket
from checkSumMethods import checkChecksum, calcChecksum, buildPacketChecksum
from headerEnums import MessageType
from constants import hr_Size, bf_Size
import socket
import math
import copy
import re
import os

global headerSize
global bufferSize

headerSize = hr_Size
bufferSize = bf_Size



def messageBuilder(listPacket:list[Packet])-> str:  # Using a list of packets recieved from the server, the method will 
                                                    # decode the bytes of data from the slices and concatonate to a singular string message
    data = ""
    for x in listPacket:
        data = data + (x.packetData.decode())
    return data


def calcPacketSize (data) -> int:               # calcPacketSize will calculate how many slices will be neede to send the data wanting to be sent
    dataSize = bf_Size - hr_Size
    byteLength = len(str(data).encode('utf-8')) 
    return int(math.ceil(byteLength/dataSize))


def listToInt(list:list)->int:                  # 
    total:str = ""
    for x in list:
        total = total + x
    return int(total)

def fileReadIn()-> str: # from the ./resources folder, it will lead the file name of each file in the folder directory
    txtfiles:str = ""
    ctr = 1
    readInFileList = os.listdir('./resources')
    for x in readInFileList:
        txtfiles = str(ctr) + ":"+str(len(x))+":"+x + "\n"+txtfiles
        ctr = ctr + 1
    txtfiles = txtfiles + "\nWhich text file would you like to see?"
    return txtfiles

def readFilesList() -> list: # readFilesList will return a list of each item's content
    fileList:list = []
    files = os.listdir('./resources') # <- this is now a list of files
    # print("[readFileList] files in list: ", files)
    for x in files:
        fileLocation = "./resources/"+x
        IOwrapperFile = open(fileLocation, "r")
        file = IOwrapperFile.read()
        fileList.append(file)
        # print("!![readFileList]!! FILE DOES NOT EXIST")
    return fileList


def buildIndexZero(builtMsg:str): # helps  previwing file index 0 response using the agreed file format

    # logic is that for each \n make a new item in the list and then split on each item
    
    PrintList:str = ""
    requestedList:list[str] = []
    requestedList = re.split("\n", builtMsg)

    for x in requestedList:
        requestedItem = re.split(":", x)
        if (len(requestedItem) == 3 ):
            PrintList  = requestedItem[0] + " - " +requestedItem[2] + "\n"+ PrintList
    PrintList = PrintList + "\n"+ requestedItem[len(requestedItem)-1]
    return PrintList    

def multiPacketHandle( socket: socket.socket, packetResend:Packet)-> list:
    #* Multi packet handler, if there is only 1 packet return packet
    
    #! build up the full message
    packetList:list[Packet] = []
    while True:
        timeoutCtr = 0
        try:
            incomingPacket = socket.recvfrom(bufferSize)

            #! check checksum
            recievedPacket:Packet = packetBuilder(incomingPacket)

            if (checkChecksum(recievedPacket)): #! <- this is a tuple

                if (incomingPacket[1] == packetResend.address):
                    if (len(packetList) == 0):
                        packetList.append(recievedPacket)

                    elif ( recievedPacket.sliceIndex == ((packetList[len(packetList)-1].sliceIndex)+1) ):
                        packetList.append(recievedPacket)
                    
                    if (packetList[len(packetList)-1].sliceIndex == packetList[len(packetList)-1].lastSliceIndex):
                        break
                    else:
                        responsePacket:Packet = copy.copy(recievedPacket)
                        responsePacket.sliceIndex += 1
                        responsePacket.checkSum = calcChecksum(buildPacketChecksum(responsePacket))
                        responsePacket.bodyLength = len(objToPacket(responsePacket))
                        socket.sendto(objToPacket(responsePacket), responsePacket.address)

        except Exception as e:
            print(e)
            timeoutCtr += 1
            if (timeoutCtr > 10 ):
                print("!!REQUEST TIMEOUT AFTER 10 TRIES!!")
            else:
                multiSendPacket(packetResend, socket)

    return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket):
    
    #* break down the message into smaller packets then send them in groups

    ctr = 1
    packetList:list[Packet] = [] # store packets here to be sent and can be reqeusted again
    dataSize = bufferSize - 19
    for x in range (packet.lastSliceIndex):
        start = x   * dataSize
        end   = (x+1)*dataSize
        if ( end > len(packet.packetData)):
            end = end-(end-len(packet.packetData))
        splitMsg = packet.packetData[start:end]
        
        packetToSend = copy.copy(packet)
        packetToSend.packetData = splitMsg
        packetToSend.sliceIndex = ctr
        packetList.append(packetToSend) 
        ctr = ctr +  1
        
    for x in packetList:
        x.checkSum = calcChecksum(buildPacketChecksum(x))
        x.bodyLength = len(objToPacket(x))        
        socket.sendto(objToPacket(x), x.address)

        # print("\nbuild packet checksum", buildPacketChecksum(x))
        # print ("\ncalcu checksum w/ build", calcChecksum(buildPacketChecksum(x)))

        # x.checkSumSetter(calcChecksum(buildPacketChecksum(x)))
        # socket.sendto(objToPacket(x), x.address)