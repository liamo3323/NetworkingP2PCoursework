import socket
from typing import Tuple
from main import BUFFERSIZE, HEAD
from header import headerCreator, MessageType

def client(connectionAddress, bufferSize): 

    # * Address where client wants to connect to
    targetIP     = connectionAddress[0]
    targetPort   = connectionAddress[1]
    fullAddress = (targetIP, targetPort)
    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    print("\nUDP client up connecting to!\nClientIP: "+str(targetIP)+"\nclientPort: "+str(targetPort)+"\n")

    # -------------------------------------------------------
    while True:
        
        initialHandshakeClient() # !client needs to do a ping to the server asking for agreed bufferSize

        # ? ----

        clientInput = input() # string input --> server 

        if (clientInput == "givelist"):
            print ()
        else:
            print ()

def initialHandshakeClient(socket: socket.socket, targetAddress: Tuple):
    initialHandshakeHeaderE = headerCreator(MessageType.h, 1)
    clientBufferSizeE = BUFFERSIZE.encode('utf-8')
    requestE = initialHandshakeHeaderE + clientBufferSizeE
    socket.sendto(requestE, targetAddress)