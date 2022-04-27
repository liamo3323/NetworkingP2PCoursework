from ipaddress import ip_address
from logging import exception
from packet_class import Packet, packetBuilder, objToPacket, checkSumSetter
from checkSumMethods import checkChecksum, calcChecksum, buildPacketChecksum
from headerEnums import MessageType
from constants import hr_Size, bf_Size
import socket
import math
import copy
import os

global headerSize
global bufferSize

headerSize = hr_Size
bufferSize = bf_Size

def messageBuilder(listPacket:list[Packet])-> str:
    data = ""
    print(len(listPacket))
    for x in listPacket:
        data = data + (x.packetData.decode())
    return data


def calcPacketSize (data) -> int:
    dataSize = bf_Size - hr_Size
    byteLength = len(str(data).encode('utf-8')) 
    return int(math.ceil(byteLength/dataSize))


def listToInt(list:list)->int:
    total:str = ""
    for x in list:
        total = total + x
    return int(total)

#! come up with better names! 

def fileReadIn()-> str:
    txtfiles:str = ""
    ctr = 1
    readInFileList = os.listdir('./resources')
    for x in readInFileList:
        txtfiles = str(ctr) + ":"+str(len(x))+":"+x + "\n"+txtfiles
        ctr = ctr + 1
    txtfiles = txtfiles + "\nWhich text file would you like to see?"
    return txtfiles

def readFilesList() -> list:
    fileList:list = []
    files = os.listdir('./resources') # <- this is now a list of files
    print("[readFileList] files in list: ", files)
    for x in files:
        fileLocation = "./resources/"+x
        IOwrapperFile = open(fileLocation, "r")
        file = IOwrapperFile.read()
        fileList.append(file)
        # print("!![readFileList]!! FILE DOES NOT EXIST")
    return fileList



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
                        print ("packet list slice index", packetList[len(packetList)-1].sliceIndex, " packet list slice max ", packetList[len(packetList)-1].lastSliceIndex)
                        break
                    else:
                        responsePacket:Packet = copy.copy(recievedPacket)
                        responsePacket.sliceIndex += 1
                        responsePacket.checkSum = calcChecksum(buildPacketChecksum(responsePacket))
                        socket.sendto(objToPacket(responsePacket), responsePacket.address)

        except Exception as e:
            print(e)
            timeoutCtr += 1
            if (timeoutCtr > 10 ):
                print("!!REQUEST TIMEOUT AFTER 10 TRIES!!")
            else:
                multiSendPacket(packetResend, socket)

    print (packetList)
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
        print("build packet checksum", buildPacketChecksum(x))
        print ("calcu checksum w/ build", calcChecksum(buildPacketChecksum(x)))
        x.checkSum = calcChecksum(buildPacketChecksum(x))
        socket.sendto(objToPacket(x), x.address)

        # print("\nbuild packet checksum", buildPacketChecksum(x))
        # print ("\ncalcu checksum w/ build", calcChecksum(buildPacketChecksum(x)))

        # x.checkSumSetter(calcChecksum(buildPacketChecksum(x)))
        # socket.sendto(objToPacket(x), x.address)