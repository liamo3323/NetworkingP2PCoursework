import socket
import os
from tokenize import String
import time

global bufferSize
global headerSize

bufferSize  = 128 # each character is a singular byte
headerSize = 8
dataSize = bufferSize-headerSize

#Todo List! 
# - ask if a message can be sent without a handshake???
# - allocate header || Header Byte format: 1- Type, 2- Package Num, 3- Total Package Num, 4- Current Package Num, 5+6- Checksum, 7+8-Future Proof ||

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
        encodedClientInput = encodeData(clientInput)
        # msg does not need to be decoded because its client input
        if (clientInput == "givelist"):
            clientSocket.send(encodedClientInput)
            requestListClient(clientSocket)
        
        else: 
            clientSocket.send(encodedClientInput)

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
    sendMessage(txtfiles, socket, hostAddress)        # socket.sendto(encodeData(txtfiles), hostAddress)

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
    sendMessage(fileData, socket, address)      #socket.sendto(encodeData(fileData), address)

####################################################################

def requestListClient(socket):
    request = socket.recvfrom(bufferSize)
    message = request[0]
    address = request[1]
    clientMessage = f"{address} || {decode(message)}"
    print(clientMessage) # printing which file I want

    fileSelection= input()
    sendMessage(fileSelection, socket, address)        #socket.sendto(encodeData(fileSelection), address) # sending back which file I want

    print("I sent da stuff waiting for return")
    dataReturn = socket.recvfrom(bufferSize)
    message = dataReturn[0]
    address = dataReturn[1]
    clientMessage = f"{decode(message)}" # seeing what is replied back
    print(clientMessage)

def encodeData(dataInputWithHeader): # Method that will take input and put it into an array and encode it
    tempArr = ""
    encodedMsg = ""

    # temp header setup
    for x in range(headerSize):
        tempArr = tempArr + str(x)
    
    # tagging data to be passed along to the header
    encodedMsg = tempArr + dataInputWithHeader

    return bytes(encodedMsg, 'utf-8')

def decode(dataInput):
    decodedData = dataInput.decode()
    message = decodedData[8:]
    return message

def checkMessageLength(message):
    return len(message.encode('utf-8'))

def sendMessage(message, socket, targetAddress):
    #socket.sendto(encodeData(fileSelection), address)
    socket.sendto(encodeData(message), targetAddress)
