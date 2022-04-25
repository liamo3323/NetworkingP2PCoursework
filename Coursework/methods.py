from ipaddress import ip_address
from logging import exception
from packet_class import Packet, packetBuilder, objToPacket
from headerEnums import MessageType
import socket
import math
import time

def messageBuilder(listPacket:list[Packet])-> str:
    data = ""
    print(len(listPacket))
    for x in listPacket:
        data = data + (x.packetData.decode())
    return data


def calcPacketSize(dataSize: int, data) -> int:
    byteLength = len(str(data).encode('utf-8')) 
    return int(math.ceil(byteLength/dataSize))


def multiPacketHandle( socket: socket.socket, bufferSize: int, packetResend:Packet)-> list:
    #* Multi packet handler, if there is only 1 packet return packet
    
    #! build up the full message

    packetList:list[Packet] = []
    while True:
        try:
            incomingPacket = socket.recvfrom(bufferSize)
            #! check checksum
            
            recievedPacket:Packet = packetBuilder(incomingPacket)
            if (checkChecksum(recievedPacket)): #! <- this is a tuple
                
                if (incomingPacket[1] == packetResend.address):
                    if (len(packetList) == 0):
                        packetList.append(recievedPacket)

                    elif ( recievedPacket.currentPacket == ((packetList[len(packetList)-1].currentPacket)+1) ):
                        packetList.append(recievedPacket)
                    
                    if (packetList[len(packetList)-1].currentPacket == packetList[len(packetList)-1].packetTot):
                        break
        except Exception as e:
            print(e)
            multiSendPacket(packetResend, socket, bufferSize)


    
    return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    
    #* break down the message into smaller packets then send them in groups

    ctr = 1
    packetList:list[Packet] = [] # store packets here to be sent and can be reqeusted again
    dataSize = bufferSize - 19
    for x in range (packet.packetTot):
        start = x   * dataSize
        end   = (x+1)*dataSize
        if ( end > len(packet.packetData)):
            end = end-(end-len(packet.packetData))
        splitMsg = packet.packetData[start:end]
        packetToSend = Packet( MessageType(packet.type), packet.currentPacket, packet.packetTot, packet.checkSum, packet.headCheckSum, packet.req, splitMsg, packet.ip, packet.port)
        packetToSend.currentPacket = ctr
        packetList.append(packetToSend) 
        ctr = ctr +  1
        
    for x in packetList:
        x.checkSum = calcChecksum(buildPacketChecksum(x))
        socket.sendto(objToPacket(x), x.address)


def calcChecksum(data:bytes)->int:
    x = 0
    for byte in data:
        x = (x + byte) & 0xFFFFFFFF
    return (((x ^ 0xFFFFFFFF) +1) & 0xFFFFFFFF)
    

def checkChecksum(packet:Packet)->bool:
    givenChecksum = packet.checkSum

    calculatedChecksum = calcChecksum(buildPacketChecksum(packet))

    print("given", givenChecksum)
    print("calculated", calculatedChecksum)

    if (givenChecksum == calculatedChecksum):
        return True
    else:
        return False

def buildPacketChecksum(packet:Packet)->bytes:
    encodedHeader = (packet.type.to_bytes(1, 'little') 
    + packet.currentPacket.to_bytes(4, 'little') 
    + packet.packetTot.to_bytes(4, 'little') 
    + (0).to_bytes(4, 'little') 
    + packet.headCheckSum.to_bytes(4, 'little')
    + packet.req.to_bytes(2, 'little'))
    return encodedHeader+packet.packetData
