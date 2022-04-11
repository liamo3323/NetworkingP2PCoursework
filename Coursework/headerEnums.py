from enum import Enum
class MessageType(Enum):
    hnd = 0 # initialHandshake
    req = 1 # request
    fin = 2 # finished data transmission
    givelist = 3 # request to request the list of document
    requestFiles = 4 # request to request specific document
    ack = 5
