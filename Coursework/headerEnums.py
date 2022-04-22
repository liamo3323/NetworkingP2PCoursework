from enum import Enum
class MessageType(Enum):
    HND = 0 # initialHandshake
    REQ = 1 # requesting something
    RES = 2 # responce to request
    GIV = 3 # returns a list of files peer has  
    