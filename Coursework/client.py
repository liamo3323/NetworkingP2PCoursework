import socket
from typing import Tuple
from headerEnums import MessageType
from packet_class import packet


buffersize = 32     # total buffer size
header = 6          # total size allocated to header


def clientStart(connectionAddress): 

    # * Address where client wants to connect to
    targetIP     = connectionAddress[0]
    targetPort   = connectionAddress[1]
    fullAddress = (targetIP, targetPort)
    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    print("\nUDP client up connecting to!\nClientIP: "+str(targetIP)+"\nclientPort: "+str(targetPort)+"\n")

    # -------------------------------------------------------
    while True:
        
        #initialHandshakeClient() # !client needs to do a ping to the server asking for agreed bufferSize

        # ? ----

        clientInput = input() # string input --> server 

        if (clientInput == "givelist"):
            packetGiveList = packet(MessageType.hnd, 0, 0, targetIP, targetPort)
        else:
            print ()

