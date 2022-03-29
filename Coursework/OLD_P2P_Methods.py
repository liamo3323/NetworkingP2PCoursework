import socket

def p2pStartClient():

    serverAddresses = specifyConnectionClient()

    msgFromClient       = "Hello, I sent from the Client"
    bytesToSend         = str.encode(msgFromClient)
    #serverAddressPort   = ("127.0.0.1", 20001)
    serverAddressPort = (serverAddresses[0], int(serverAddresses[1]))
    bufferSize          = 1024 #temp buffer size for now 

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.connect(serverAddressPort)
    UDPClientSocket.send(bytesToSend)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)

def specifyConnectionClient():
    ip = input("Client: What ip would you like to connect to?: ")
    port = input("Client: What port would you like to connect to?: ")

    if (ip == "localhost"):
        ip = "127.0.0.1"
         
    return [ip,port]

def p2pStartServer():

    serverAddresses = specifyConnectionServer()

    localIP     = serverAddresses[0]
    localPort   = int(serverAddresses[1])
    bufferSize  = 1024

    msgFromServer       = "Hello, I sent from the Server"
    bytesToSend         = str.encode(msgFromServer)

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort)) 
    print("UDP server up and listening for client!")

    # Listen for incoming datagrams
    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client: {}".format(message)
        clientIP  = "Client IP Address: {}".format(address)
        
        print(clientMsg)
        print(clientIP)

        # Sending a reply back to client
        UDPServerSocket.sendto(bytesToSend, address)


def specifyConnectionServer():
    ip = input("Server: What ip would you like to host on?: ")
    port = input("Server: What port would you like to host on?: ")

    if (ip == "localhost"):
        ip = "127.0.0.1"
         
    return [ip,port]