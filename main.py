from server import serverStart
from client import clientStart
from threading import Thread
import sys
import re

# todo list:
# - format list
# - check what checksum header includes
# - add comments around the place
# - check with RFC what else  is there to do? 

def configuration():

    # args will be the selected configuration desired! 
    # arg 1 will be host arg 2 will be connect

    hostIP:str = ""
    hostPort:int = 0
    ConnIP:str = ""
    ConnPort:int = 0

    try:
        if (sys.argv[1] == 'a' and sys.argv[2] == 'b'):
            return(("127.0.0.1",30000), ("127.0.0.2", 30001))

        elif (sys.argv[1] == 'b' and sys.argv[2] == 'a'):
            return(("127.0.0.2", 30001),("127.0.0.1",30000))

        elif (sys.argv[1] == "ollie"):
            hostIP:str = "0.0.0.0"
            hostPort:int = 6969
            ConnIP:str = "10.77.38.136"
            ConnPort:int = 10000
            return((hostIP,hostPort),(ConnIP,ConnPort))
        
        elif (sys.argv[1] != '' and sys.argv[2] != ''):
             return (splitArg(sys.argv[1]),(splitArg(sys.argv[1])))
    
    except:
        print("-----------------------------\n[main] No Arguments detected!\n-----------------------------\n")
        hostIP      = input("[main] What ip would you like to host on?: ")
        hostPort    = int(input("[main] What port would you like to host on?: "))
        
        ConnIP      = input("[main] What ip would you like to connect to?: ")
        ConnPort    = int(input("[main] What port would you like to connect to?: "))
        return ((hostIP, hostPort),(ConnIP,ConnPort))

def splitArg(argument:str):
    args = re.split(":", argument)
    return(args[0],int(args[1]))

config = configuration()

# threading to run a client instance and server instance for PEER to PEER to work
if __name__ == '__main__':
    Thread(target = serverStart, args=(config[0],)).start()
    Thread(target = clientStart, args=(config[1],)).start()