from packet_class import Packet, packetBuilder
from headerEnums import MessageType
import socket
import math

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
    packetList = []
    packet = packetBuilder( socket.recvfrom(bufferSize))
    packetLoops = packet.packetTot
    packetList.append(packet)

    #! build up the full message

    while True:
        recievedPacket = packetBuilder( socket.recvfrom(bufferSize))
        packetList.append(recievedPacket)
        akg = recievedPacket
        akg.type = MessageType.ACK
        socket.sendto(akg.encodedHeader, akg.address)
        if (akg.currentPacket == akg.packetTot):
            break
    akg.type = MessageType.FIN
    socket.sendto(akg.encodedHeader, akg.address)
    
    return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    #? logic is that request will always send the first packtet NOT send a zero.th packet 

    #* break down the message into smaller packets then send them in groups
    
    packetList = [] # store packets here to be sent and can be reqeusted again
    for x in range (packet.packetTot):
        start = x   * bufferSize
        end   = x+1 * bufferSize
        if ( end > len(packet.packetData)):
            end = end-(end-len(packet.packetData))
        splitMsg = packet.packetData[start:end]
        packetToSend = Packet( MessageType(packet.type), packet.packetTot, splitMsg, packet.ip, packet.port)
        packetList.append(packetToSend)
    ctr = 1
    for x in packetList:
        x.currentPacket = ctr
        ctr = ctr + 1

    socket.send(packetList[0].packet, packetList[0].address)
    while True:
        akg = packetBuilder( socket.recvfrom(bufferSize))
        if (akg.type == MessageType.FIN):
            break
        socket.send(packetList[akg.currentPacket].packet, packetList[akg.currentPacket].address)

    print("All packets sent!!")