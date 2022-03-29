import socket

def p2pStartClient(client):

    msgFromClient       = "Hello, I sent from the Client"
    bytesToSend         = str.encode(msgFromClient)
    #serverAddressPort   = ("127.0.0.1", 20001)
    serverAddressPort = (client[0], client[1])
    bufferSize = 1024 

    # Create a UDP socket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using socket
    UDPClientSocket.connect(serverAddressPort)

    while True:

        clientMsg = str.encode(input())
        UDPClientSocket.send(clientMsg)

def p2pStartServer(server):

    localIP     = server[0]
    localPort   = server[1]
    bufferSize  = 1024

    msgFromServer       = "Hello, I sent from the Server"
    bytesToSend         = str.encode(msgFromServer)

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort)) 
    print("\n UDP server up and listening for client! \n")

    # Listen for incoming datagrams
    while True:

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        clientMessage = f"{address} || {message}"
        print(clientMessage)
