from packet_class import Packet
import socket
import math

def calcPacketSize(dataSize: int, data) -> int:
    byteLength = len(str(data).encode('utf-8')) 
    return int(math.ceil(byteLength/dataSize))

def multiPacketHandle(packet: Packet):
    #* Multi packet handler, if there is only 1 packet return packet

    if (packet.packetTot == 1):
        return(packet)
    else:
        #! build up the full message
        print()

def multiSendPacket(packet: Packet, socket: socket.socket, bufferSize: int):
    if (packet.packetTot == 1):
        socket.sendto(packet.packet, packet.address)
    else:
        #* break down the message into smaller packets then send them in groups
        
        #- buf=12 msg = 34 | send 12, 12, 10
        #- 0-12, 12-24, 24-34

        packetList = []
        for x in range (packet.packetTot):

            start = x   * bufferSize
            end   = x+1 * bufferSize
            if ( end > len(packet.packetData)):
                end = end-(end-len(packet.packetData))
            splitMsg = packet.packetData[start:end]
            packetList.append(Packet(packet.type, x, packet.packetTot, splitMsg, packet.ip, packet.port))
        