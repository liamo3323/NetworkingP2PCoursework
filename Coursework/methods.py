from packet_class import Packet, packetBuilder
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
    packetList.append(packet)

    if (packet.packetTot == 1):
        return(packetList)
    else:
        #! build up the full message
        for x in range (packet.packetTot):
            recievedPacket = packetBuilder( socket.recvfrom(bufferSize))
            packetList.append(recievedPacket)
        
        return(packetList)

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    #? logic is that request will always send the first packtet NOT send a zero.th packet 

    if (packet.packetTot == 1):
        socket.sendto(packet.packet, packet.address)
    else:
        #* break down the message into smaller packets then send them in groups
        
        #- buf=12 msg = 34 | send 12, 12, 10
        #- 0-12, 12-24, 24-34

        packetList = [] # store packets here to be sent and can be reqeusted again
        for x in range (packet.packetTot):
            print("sending Packets!")
            start = x   * bufferSize
            end   = x+1 * bufferSize
            if ( end > len(packet.packetData)):
                end = end-(end-len(packet.packetData))
            splitMsg = packet.packetData[start:end]
            packetList.append(Packet(packet.type, x, packet.packetTot, splitMsg, packet.ip, packet.port))
        print("All packets sent!!")