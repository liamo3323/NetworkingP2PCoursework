from server import serverStart
from client import clientStart
from threading import Thread
import sys

# COPY PASTE
# python3 main.py 20001 20000
# python3 main.py 20000 20001

# todo:
#! checking if packet recieved is correct via checksum

#! Client makes a request which loads the file then any following akg will be responding to requests
#! if packet id is 0 then return list

#? timeout for request
#? Handle - >certain that we recieved in the right increment

# client requests a file and asks for the first packet
# server receives reqeust and grabs first packet of file (server knows how many slices) and responds first OF e.g. 10
# client waits until it recieves the last slice 10th and waits for the slice for like 10 seconds 
# client DOESNT NEED to send a ACK 
# timeout for request
# request 


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