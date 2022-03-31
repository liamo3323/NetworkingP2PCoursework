import socket
import os

bufferSize  = 256

def p2pStartClient(client):
    serverAddressPort = (client[0], client[1])
    clientIP     = client[0]
    clientPort   = client[1]

    readDirectory()

    # Create a UDP socket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using socket
    UDPClientSocket.connect(serverAddressPort)
    print("\nUDP client up!\nClientIP: "+str(clientIP)+"\nclientPort: "+str(clientPort)+"\n")

    while True:
        clientMsg = str.encode(input())
        UDPClientSocket.send(clientMsg)

        if (clientMsg.decode() == "givelist"):
            returnMsg = UDPClientSocket.recvfrom(bufferSize)
            message = returnMsg[0]
            address = returnMsg[1]
            returnMessage = f"{address} || {message.decode()}"
            print(returnMessage)

def p2pStartServer(server):
    serverIP     = server[0]
    serverPort   = server[1]


    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((serverIP, serverPort)) 
    print("\nUDP Server up! \nServerIP: "+str(serverIP)+"\nServerPort: "+str(serverPort)+"\n")

    # Listen for incoming datagrams
    while True:

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        clientMessage = f"{address} || {message.decode()}"
        print(clientMessage)

        if (message.decode() == "givelist"):
            # this will respond to client A from server B...
            array = ["A","B","C","D"] 
            itemList = ""
            for x in array:
                itemList = itemList + " " + x 
            requestMsg = str.encode(itemList)
            UDPServerSocket.send(requestMsg)

def readDirectory():
    txtfiles = []
    files = os.listdir('./resources')
    print(files)
