import socket
import os
from tokenize import String

bufferSize  = 256

def p2pStartClient(client):
    serverAddressPort = (client[0], client[1])
    clientIP     = client[0]
    clientPort   = client[1]

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.connect(serverAddressPort)
    print("\nUDP client up connecting to!\nClientIP: "+str(clientIP)+"\nclientPort: "+str(clientPort)+"\n")

    while True:
        decodedMsg = input()
        clientMsg = str.encode(decodedMsg)
        UDPClientSocket.send(clientMsg)

        if (decodedMsg == "givelist"):
            request = UDPClientSocket.recvfrom(bufferSize)
            message = request[0]
            address = request[1]
            clientMessage = f"{address} || {message.decode()}"
            print(clientMessage) # printing which file I want
            
            whichFile= input()
            UDPClientSocket.sendto(str.encode(whichFile), address) # sending back which file I want

            print("I sent da stuff waiting for return")
            dataReturn = UDPClientSocket.recvfrom(bufferSize)
            message = dataReturn[0]
            address = dataReturn[1]
            clientMessage = f"{message.decode()}" # seeing what is replied back
            print(clientMessage)


def p2pStartServer(server):
    serverIP     = server[0]
    serverPort   = server[1]

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((serverIP, serverPort)) 
    print("\nUDP Server up! \nServerIP: "+str(serverIP)+"\nServerPort: "+str(serverPort)+"\n")

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        clientMessage = f"{address} || {message.decode()}"
        print(clientMessage)

        if (message.decode() == "givelist"):
            txtfiles = ""
            files = os.listdir('./resources')
            for x in files:
                txtfiles = x + ", " + txtfiles
            txtfiles = "["+ txtfiles +"]" + "\nWhich text file would you like to see?"
            UDPServerSocket.sendto(str.encode(txtfiles), address)

            reply = UDPServerSocket.recvfrom(bufferSize) # this will recieve a number for which file we want to see
            message = reply[0]
            address = reply[1]

            requestedNumberDecoded = message.decode()
            requestedNumberInt = int(requestedNumberDecoded)
            requestedFileName = files[requestedNumberInt-1]
            print(requestedFileName)
            fileLocation = "./resources/"+requestedFileName
            txt = open(fileLocation, "r")
            fileData = txt.read() 
            print(fileData)
            UDPServerSocket.sendto(str.encode(fileData), address)