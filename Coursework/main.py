from server import serverStart
from client import clientStart
from threading import Thread
import sys

# COPY PASTE
# python3 main.py 20001 20000
# python3 main.py 20000 20001

# todo:
# - whenever a packet is going to be recieved it must check how many are going to be recieved 
    #- first packet will be 0th packet and start the request
    #- then it will keep on sending packets until finished
    #- while packets are being recieved the client will reply with ack
        #- if server doesn't recieve ack resend that packet
# - request and recieving of list of available files...
#- gotta think about how to rebuild the packet of data lol
#- maybe implement a max bufferSize ? 
#- change all for loops with while loops with AKGs
#- add AKG packets in reply

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
    Thread(target = serverStart, args=(hostAddress,)).start()
    Thread(target = clientStart, args=(connectionAddress,)).start()