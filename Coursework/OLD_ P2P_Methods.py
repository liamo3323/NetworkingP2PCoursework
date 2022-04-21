import socket
import os
from tokenize import String
import time
import math

global bufferSize
global headerSize
global dataSize

bufferSize  = 128 # each character is a singular byte
headerSize = 8
dataSize = bufferSize-headerSize

#Todo List! 
# -|| Header Byte format: 1- Type, 2- Package Num, 3- Total Package Num, 4- Current Package Num, 5+6- Checksum, 7+8-Future Proof ||

#!################ Client Loop #################

def p2pStartClient(connectTo):
    targetAddress = (connectTo[0], connectTo[1]) # this is the ip and port of who we want to connect to! 
    targetIP     = connectTo[0]
    targetPort   = connectTo[1]

    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    #clientSocket.connect(targetAddress)
    print("\nUDP client up connecting to!\nClientIP: "+str(targetIP)+"\nclientPort: "+str(targetPort)+"\n")

    while True:
        clientInput = input() # client will always request user input

        if (clientInput == "givelist"):
            sendMessage(clientInput, clientSocket, targetAddress)
            requestListClient(clientSocket)
        
        else: 
            sendMessage(clientInput, clientSocket, targetAddress)

#!################ Server Loop #################

def p2pStartServer(host): # This is the ip and address of where the host is 
    hostIP = host[0]
    hostPort = host[1]

    connectedIP = 0
    connectedPort = 0

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort)) 
    print("\nUDP Server up! \nServerIP: "+str(hostIP)+"\nServerPort: "+str(hostPort)+"\n")

    while True:
        connectedClient = serverSocket.recvfrom(bufferSize)
        clientMessage = connectedClient[0]
        clientAddress = connectedClient[1]
        clientMessageDecoded = decode(clientMessage)

        if (clientMessageDecoded == "givelist"):
            requestListServer(serverSocket, clientAddress)
        
        else:
            #receiveMessage(clientMessage)
            receiveMessage(serverSocket)
            print(": "+clientMessageDecoded)

#!###################################################################

def requestListServer(socket, hostAddress):

    ########## file manipulation ##########
    txtfiles = ""
    files = os.listdir('./resources')
    for x in files:
        txtfiles = x + ", " + txtfiles
    txtfiles = "["+ txtfiles +"]" + "\nWhich text file would you like to see?"
    sendMessageEncode(txtfiles, socket, hostAddress) 

    ######### awaiting reply from file list ##########
    reply = socket.recvfrom(bufferSize) # this will recieve a number for which file we want to see
    message = reply[0]
    address = reply[1]

    requestedNumberDecoded = decode(message)
    requestedNumberInt = int(requestedNumberDecoded)
    requestedFileName = files[requestedNumberInt-1]
    print(requestedFileName)

    fileData = txt.read() 
    print("Sent requested file!")
    sendMessage(fileData, socket, address) 

####################################################################

def requestListClient(socket):
    request = socket.recvfrom(bufferSize)
    message = request[0]
    address = request[1]
    clientMessage = f"{address} || {message.decode()}"
    print(clientMessage) # printing which file I want

    fileSelection= input()
    sendMessage(fileSelection, socket, address) 

    dataReturn = socket.recvfrom(bufferSize)
    message = dataReturn[0]
    address = dataReturn[1]
    clientMessage = f"{message.decode()}" # seeing what is replied back
    print(clientMessage)

def sendMessage(decodedData, socket, targetAddress):

    # * when making an encoded message the header and body of the data is being encoded in the same section 

    type = 0     
    packetTot = 0
    currentPacket = 0
    checkSum = 0
    extra = 0

    byteLength = len(decodedData.encode('utf-8')) # length of data that needs to be sent
    packetTot = int(math.ceil(byteLength/dataSize)) # number of packets that needs to be sent         

    handShakePacket(packetTot, socket, targetAddress)

    for x in range (packetTot): # ! still gotta add packet type & checksum  
        start = x*dataSize
        end = x+1*dataSize
        if (int(end) > int(byteLength)):
            end = start+(byteLength-start)
        decodedPacketData = decodedData[start:end]

        # ---------------- Initializing Header Part -----------------

        currentPacket = x

        encodedHeader = (type.to_bytes(1, 'little') 
        + currentPacket.to_bytes(1, 'little') 
        + packetTot.to_bytes(1, 'little') 
        + checkSum.to_bytes(1, 'little') 
        + extra.to_bytes(headerSize-4, 'little'))

        encodedFinalMessage = encodedHeader + bytes(decodedPacketData, 'utf-8')
        socket.sendto(encodedFinalMessage, targetAddress)
    
    # todo: gotta do server side constant listening 

def handShakePacket(totalPacket, socket, address):
    type = 0    
    packetTot = totalPacket
    currentPacket = 0
    checkSum = 0
    extra = 0

    encodedHeader = (type.to_bytes(1, 'little') 
    + currentPacket.to_bytes(1, 'little') 
    + packetTot.to_bytes(1, 'little') 
    + checkSum.to_bytes(1, 'little') 
    + extra.to_bytes(headerSize-4, 'little'))

    socket.sendto(encodedHeader, address)


def receiveMessage(socket):
    numOfPacket = socket.recvfrom(bufferSize)
    packets = (decode(numOfPacket))[2]
    finishedFile = ""
    for x in range(packets):
        packet = socket.recvfrom(bufferSize)

        header = packet[:8]
        data = packet[8:]
        finishedFile += data
