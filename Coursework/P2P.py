from P2P_Methods import p2pStartClient, p2pStartServer
from threading import Thread

def specifyConnectionServer():
    ip = input("Server: What ip would you like to host on?: ")
    port = input("Server: What port would you like to host on?: ")

    if (ip == "lh1"):
        ip = "127.0.0.1"
    
    elif (ip == "lh0"):
        ip = "127.0.0.0"   

    if (port == "a"):
        port = "2000"
    
    elif (port == "b"):
        port = "2001"

    return [ip, int(port)]
def specifyConnectionClient():
    ip = input("Client: What ip would you like to connect to?: ")
    port = input("Client: What port would you like to connect to?: ")

    if (ip == "lh1"):
        ip = "127.0.0.1"
    
    elif (ip == "lh0"):
        ip = "127.0.0.0"    

    if (port == "a"):
        port = "2000"
    
    elif (port == "b"):
        port = "2001"

         
    return [ip, int(port)]

client = specifyConnectionClient()
server = specifyConnectionServer()

if __name__ == '__main__':
    Thread(target = p2pStartServer, args=(server,)).start()
    Thread(target = p2pStartClient, args=(client,)).start()


