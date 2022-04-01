import socket
import os
from tokenize import String

bufferSize  = 128 #each character is a singular byte
headerSize = 4
dataSize = bufferSize-headerSize

#Todo List! 
# - ask if a message can be sent without a handshake???
# - allocate header
# - make a Verb --> header + data format style 
# - handshake command

def p2pStartClient(client):
    serverAddressPort = (client[0], client[1]) # this is the ip and port of who we want to connect to! 
    clientIP     = client[0]
    clientPort   = client[1]

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.connect(serverAddressPort)
    print("\nUDP client up connecting to!\nClientIP: "+str(clientIP)+"\nclientPort: "+str(clientPort)+"\n")

    while True:
        decodedMsg = input() # client will always want to send user input

        if (decodedMsg == "givelist"):
            requestListClient(UDPClientSocket)
        
        if (decodedMsg == "hand"):
            UDPClientSocket.send(str.encode("handshake request"))
            
            bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
            address = bytesAddressPair[1]
            connectedIP = address[0]
            connectedPort = address[1]
            print("Connecting request from "+str(connectedIP)+" port: "+str(connectedPort))

        else:
            UDPClientSocket.send(str.encode(decodedMsg))


def p2pStartServer(server):
    serverIP        = server[0]
    serverPort      = server[1]

    connectedIP     = 0
    connectedPort   = 0

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((serverIP, serverPort)) 
    print("\nUDP Server up! \nServerIP: "+str(serverIP)+"\nServerPort: "+str(serverPort)+"\n")

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMessageDecoded = f": {message.decode()}"

        if (clientMessageDecoded == "givelist" and connectedIP > 0):
            requestListServer(UDPServerSocket, (serverIP, serverPort))
        
        if (clientMessageDecoded == "hand"):
            connectedIP = address[0]
            connectedPort = address[1]
            connectedaddress = (connectedIP, connectedPort)
            print("Connecting request from "+str(connectedIP)+" port: "+str(connectedPort))
            UDPServerSocket.sendto(str.encode("Connecting to "+str(connectedIP)+" port: "+str(connectedPort)), connectedaddress)

        else:
            print(clientMessageDecoded)


def requestListServer(socket, address):
    txtfiles = ""
    files = os.listdir('./resources')
    for x in files:
        txtfiles = x + ", " + txtfiles
    txtfiles = "["+ txtfiles +"]" + "\nWhich text file would you like to see?"
    socket.sendto(str.encode(txtfiles), address)

    reply = socket.recvfrom(bufferSize) # this will recieve a number for which file we want to see
    message = reply[0]
    address = reply[1]

    requestedNumberDecoded = message.decode()
    requestedNumberInt = int(requestedNumberDecoded)
    requestedFileName = files[requestedNumberInt-1]
    print(requestedFileName)
    fileLocation = "./resources/"+requestedFileName
    txt = open(fileLocation, "r")
    fileData = txt.read() 
    print("Sent requested file!")
    socket.sendto(str.encode(fileData), address)

def requestListClient(socket):
    request = socket.recvfrom(bufferSize)
    message = request[0]
    address = request[1]
    clientMessage = f"{address} || {message.decode()}"
    print(clientMessage) # printing which file I want
    
    whichFile= input()
    socket.sendto(str.encode(whichFile), address) # sending back which file I want

    print("I sent da stuff waiting for return")
    dataReturn = socket.recvfrom(bufferSize)
    message = dataReturn[0]
    address = dataReturn[1]
    clientMessage = f"{message.decode()}" # seeing what is replied back
    print(clientMessage)