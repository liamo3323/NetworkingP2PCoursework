import socket
from typing import Tuple
from headerEnums import MessageType
from packet_class import packet
from methods import calcPacketSize
from constants import hr_Size, bf_Size
bufferSize = bf_Size
headerSize = hr_Size

def clientStart(connectionAddress): 

    # * Address where client wants to connect to
    targetIP     = connectionAddress[0]
    targetPort   = connectionAddress[1]
    fullAddress = (targetIP, targetPort)
    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    print("\nUDP client up connecting to!\nClientIP: "+str(targetIP)+"\nclientPort: "+str(targetPort)+"\n")

    # -------------------------------------------------------
    while True:
        
        data = str(bf_Size)
        packetDataSize = bf_Size - hr_Size
        packetInitialHandshake = packet(MessageType.hnd, calcPacketSize(packetDataSize,data) , data.encode('utf-8'), targetIP, targetPort)
        initialHandshakeClient(clientSocket, packetInitialHandshake) 
        
        # ? ----

        clientInput = input() # string input --> server 

        if (clientInput == "givelist"):
            packetGiveList = packet(MessageType.givelist, 0, 0, targetIP, targetPort)
        
        else:
            print ("WRONG!")

def initialHandshakeClient(socket: socket.socket, packet: packet, ):
    socket.sendto(packet.packet, packet.address)
    initialHandshake = socket.recvfrom(bufferSize)

