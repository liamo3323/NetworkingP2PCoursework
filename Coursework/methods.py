from ipaddress import ip_address
from packet_class import Packet, packetBuilder, objToPacket
from headerEnums import MessageType
import socket
import math
import time

def messageBuilder(listPacket:list)-> str:
    data = ""
    print(len(listPacket))
    for x in listPacket:
        data = data + (x.packetData.decode())
    return data

def calcPacketSize(dataSize: int, data) -> int:
    byteLength = len(str(data).encode('utf-8')) 
    print("encoded message - ", str(data).encode('utf-8') )
    print("length of encoded message - ", len(str(data).encode('utf-8')), "divided by size - ", dataSize)
    return int(math.ceil(byteLength/dataSize))

def multiPacketHandle( socket: socket.socket, bufferSize: int)-> list:
    #* Multi packet handler, if there is only 1 packet return packet
    
    #! build up the full message

    packetList = []
    while True:

        recievedPacket = packetBuilder( socket.recvfrom(bufferSize))
        packetList.append(recievedPacket)
        akg = recievedPacket
        socket.sendto(akg.encodedHeader, akg.address)
        if (akg.currentPacket == akg.packetTot):
            break
    
    return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    
    #* break down the message into smaller packets then send them in groups

    ctr = 1
    packetList = [] # store packets here to be sent and can be reqeusted again
    dataSize = bufferSize - 19
    for x in range (packet.packetTot):
        start = x   * dataSize
        end   = (x+1)*dataSize
        if ( end > len(packet.packetData)):
            end = end-(end-len(packet.packetData))
        splitMsg = packet.packetData[start:end]
        packetToSend = Packet( MessageType(packet.type), packet.currentPacket, packet.packetTot, packet.checkSum, packet.headCheckSum, packet.req, splitMsg, packet.ip, packet.port)
        packetToSend.currentPacket = ctr
        packetList.append(packetToSend) # <-- main message is broken up into this list
        ctr = ctr +  1

    ctr = 0
    while True: #! this doesnt support ack not returning yet! 

        #print("sending: ", objToPacket(packetList[ctr]))

        tracker = packetList[ctr]
        socket.sendto(objToPacket(packetList[ctr]), packetList[ctr].address)
        akg = packetBuilder( socket.recvfrom(bufferSize))
        print(akg.currentPacket)
        if (akg.currentPacket == akg.packetTot):
            break
        ctr = ctr + 1