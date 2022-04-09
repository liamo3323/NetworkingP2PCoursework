from server import server
from client import client
from threading import Thread
import sys

BUFFERSIZE = 32     # total buffer size
HEADER = 6          # total size allocated to header

# COPY PASTE
# python3 main.py 20001 20000
# python3 main.py 20000 20001

# todo:
# - Agree on a buffer size (maybe use the smallest bufferSize betwewen the 2)
# - initial handshake needs to exchange an agreed buffer size
#       - there needs to be a minimum buffer size of at least 16 so that it is possible to swap bufersizes 

# ? FUTURE
    # ? checksum

def specifyConnectionServer():

    #sys arg[1] is server port hosting
    try:
        if (sys.argv[1] != ""):
            return ["127.0.0.1", int(sys.argv[1])]
    except:
        print()
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

    #sys arg[2] is client port connection
    try: 
        if (sys.argv[2] != ""):
            return ["127.0.0.1", int(sys.argv[2])]
    except:
        print()
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

connectionAddress = specifyConnectionClient()
hostAddress = specifyConnectionServer()

if __name__ == '__main__':
    Thread(target = server, args=(hostAddress,)).start()
    Thread(target = client, args=(connectionAddress,)).start()