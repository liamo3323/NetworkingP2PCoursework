from enum import Enum
class MessageType(Enum):
    HND = 0 # initialHandshake
    REQ = 1 # request
    FIN = 2 # finished data transmission
    GIVELIST = 3 # request to request the list of document
    REQUESTFILES = 4 # request to request specific document
    ACK = 5