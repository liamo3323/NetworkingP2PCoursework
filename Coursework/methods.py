from ipaddress import ip_address
from packet_class import Packet, packetBuilder
from headerEnums import MessageType
import socket
import math
import time

def messageBuilder(listPacket:list)-> str:
    data = ""
    for x in listPacket:
        data = data + (x.packetData.decode())
    return data

def calcPacketSize(dataSize: int, data) -> int:
    byteLength = len(str(data).encode('utf-8')) 
    return int(math.ceil(byteLength/dataSize))

def multiPacketHandle( socket: socket.socket, bufferSize: int)-> list:
    #* Multi packet handler, if there is only 1 packet return packet
    
    #! build up the full message

    packetList = []
    while True:

        recievedPacket = packetBuilder( socket.recvfrom(bufferSize))
        packetList.append(recievedPacket)

        #print("AKG TOT - ", recievedPacket.packetTot, "  AKG CUR - ", recievedPacket.currentPacket)

        akg = recievedPacket
        akg.type = MessageType.ACK

        socket.sendto(akg.encodedHeader, akg.address)
        if (akg.currentPacket == akg.packetTot):
            break
    
    return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    
    #* break down the message into smaller packets then send them in groups

    ctr = 1
    packetList = [] # store packets here to be sent and can be reqeusted again
    for x in range (packet.packetTot):
        start = x   * bufferSize
        end   = x+1 * bufferSize
        if ( end > len(packet.packetData)):
            end = end-(end-len(packet.packetData))
        splitMsg = packet.packetData[start:end]
        packetToSend = Packet( MessageType(packet.type), packet.currentPacket, packet.packetTot, packet.checkSum, packet.headCheckSum, packet.req, splitMsg, packet.ip, packet.port)
        packetToSend.currentPacket = ctr
        packetList.append(packetToSend) # <-- main message is broken up into this list
        ctr = ctr +  1
        time.sleep(1)



    ctr = 0
    while True: #! this doesnt support ack not returning yet! 
        socket.sendto(packetList[ctr].packet, packetList[ctr].address)
        akg = packetBuilder( socket.recvfrom(bufferSize))
        print("current packet count: --", akg.currentPacket, "packet total: --", akg.packetTot)
        if (akg.currentPacket == akg.packetTot):
            break
        ctr = ctr + 1

    print("All packets sent!!")