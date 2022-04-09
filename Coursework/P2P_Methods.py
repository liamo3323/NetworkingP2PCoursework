import socket
import os
from tokenize import String
import time

global bufferSize
global headerSize
global dataSize

bufferSize  = 128 # each character is a singular byte
headerSize = 8
dataSize = bufferSize-headerSize

#Todo List! 
# - ask if a message can be sent without a handshake???
# *|| Header Byte format: 1- Type, 2- Package Num, 3- Total Package Num, 4- Current Package Num, 5+6- Checksum, 7+8-Future Proof ||

# - handshake command

################# Client Loop #################

def p2pStartClient(connectTo):
    targetAddress = (connectTo[0], connectTo[1]) # this is the ip and port of who we want to connect to! 
    targetIP     = connectTo[0]
    targetPort   = connectTo[1]

    clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    clientSocket.connect(targetAddress)
    print("\nUDP client up connecting to!\nClientIP: "+str(targetIP)+"\nclientPort: "+str(targetPort)+"\n")

    while True:
        clientInput = input() # client will always request user input
        # msg does not need to be decoded because its client input
        if (clientInput == "givelist"):
            clientSocket.send(encodeData(clientInput))
            requestListClient(clientSocket)
        
        else: 
            clientSocket.send(encodeData(clientInput))

################# Server Loop #################

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
        
        # if (clientMessageDecoded == "hand"):
        #     connectedIP = address[0]
        #     connectedPort = address[1]
        #     connectedaddress = (connectedIP, connectedPort)
        #     print("Connecting request from "+str(connectedIP)+" port: "+str(connectedPort))
        #     serverSocket.sendto(encodeData("Connecting to "+str(connectedIP)+" port: "+str(connectedPort)), connectedaddress)

        else:
            print(": "+clientMessageDecoded)

####################################################################

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
    fileLocation = "./resources/"+requestedFileName
    txt = open(fileLocation, "r")
    fileData = txt.read() 
    print("Sent requested file!")
    sendMessageEncode(fileData, socket, address) 

####################################################################

def requestListClient(socket):
    request = socket.recvfrom(bufferSize)
    message = request[0]
    address = request[1]
    clientMessage = f"{address} || {decode(message)}"
    print(clientMessage) # printing which file I want

    fileSelection= input()
    sendMessageEncode(fileSelection, socket, address) 

    dataReturn = socket.recvfrom(bufferSize)
    message = dataReturn[0]
    address = dataReturn[1]
    clientMessage = f"{decode(message)}" # seeing what is replied back
    print(clientMessage)

def decode(dataInput):
    decodedData = dataInput.decode()
    message = decodedData[8:]
    return message

def sendMessageEncode(decodedData, socket, targetAddress):

    # * when making an encoded message the header and body of the data is being encoded in the same section 

    type = 0             # ? Not sure what this is gotta ask
    packetTot = 0
    currentPacket = 0
    checkSum = 0
    extra = 0

    byteLength = len(decodedData.encode('utf-8')) # length of data that needs to be sent
    #  dataSize = bufferSize-headerSize
    packetNum = (byteLength/dataSize)+1 # number of packets that needs to be sent         
    
    #for loop to send divided up packets 
    # I should be using [?:?] function to divide up the packets... 
    for x in range (packetNum):
        # * imagine 2 packets for size 180 so 120 and 60 so its from 0:120 then 120:180 --> so its loop counter - 1 times dataSize : loop counter times dataSize if shooting data do + missing amount
        # ! -- Please make this not scuffed --
        loopCtr = 0
        start = (loopCtr-1)*dataSize
        end = loopCtr*dataSize
        if (end > byteLength):
            end = start+(byteLength-start)
        # ! ----------------------------------
        decodedPacketData = decodedData[start:end]
        
        encodedPacketData = bytes(decodedPacketData, 'utf-8')


        # * 

        # ! THE FINAL STEP
        socket.sendto(encodedPacketData, targetAddress)
    
    # todo: gotta do server side constant listening 

def encodeData(dataInputWithHeader, packetTot, currentPacket): # Method that will take input and put it into an array and encode it

    type = 0             # ? Not sure what this is gotta ask
    packetTot = 0
    currentPacket = 0
    checkSum = 0
    extra = 0

    byteHeader = (type.to_bytes(1, 'little') 
    + currentPacket.to_bytes(1, 'little') 
    + packetTot.to_bytes(1, 'little') 
    + checkSum.to_bytes(1, 'little') 
    + extra.to_bytes(headerSize-2, 'little'))

    header = bytearray(byteHeader)
    # ! they are both byte arrays so TECHNICALLY should be able to concattonate
    encodedHeader.append(encodedMsg)
    
    
    return encodedHeader
