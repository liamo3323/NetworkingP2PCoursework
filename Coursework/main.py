from server import serverStart
from client import clientStart
from threading import Thread
import sys

# todo list:
# - format list
# - make a congif file! 
# - check what checksum header includes
# - clean up code a little but 
# - add comments around the place
# - check with RFC what else  is there to do? 
# - ask about zeroth index  

def specifyConnectionServer(): #function to ask for user input on PEER hosting IP and PORT
    try:
        if (sys.argv[1] != ""):
            return ["127.0.0.1", int(sys.argv[1])]
    except:
        print()
    ip = input("Server: What ip would you like to host on?: ")
    port = input("Server: What port would you like to host on?: ")

    # lh1 and lh0 are 2 different local host values for testing purposes
    # ports 'a' and 'b' are also for testing purposes
    if (ip ==  "ollie"):
        return ["0.0.0.0", 6969]

    if (ip == "lh1"):
        ip = "127.0.0.1"
    
    elif (ip == "lh0"):
        ip = "127.0.0.0"   

    if (port == "a"):
        port = "2000"
    
    elif (port == "b"):
        port = "2001"

    return [ip, int(port)]

def specifyConnectionClient(): #function to ask for user input on IP and PORT PEER will connect to
    try: 
        if (sys.argv[2] != ""):
            return ["127.0.0.1", int(sys.argv[2])]
    except:
        print()
    ip = input("Client: What ip would you like to connect to?: ")
    port = input("Client: What port would you like to connect to?: ")

    # lh1 and lh0 are 2 different local host values for testing purposes
    # ports 'a' and 'b' are also for testing purposes

    if (ip ==  "ollie"):
        return ["10.77.38.136", 10000]

    if (ip == "lh1"):
        ip = "127.0.0.1"
    
    elif (ip == "lh0"):
        ip = "127.0.0.0"    

    if (port == "a"):
        port = "2000"
    
    elif (port == "b"):
        port = "2001"

    return [ip, int(port)]

# host location and connecting address are always asked before creating threads 
connectionAddress = specifyConnectionClient()
hostAddress = specifyConnectionServer()

# threading to run a client instance and server instance for PEER to PEER to work
if __name__ == '__main__':
    Thread(target = serverStart, args=(hostAddress,)).start()
    Thread(target = clientStart, args=(connectionAddress,)).start()