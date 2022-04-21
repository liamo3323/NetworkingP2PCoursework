from enum import Enum
class MessageType(Enum):
    HND = 0 # initialHandshake
    REQ = 1 # requesting something
    RES = 2 # responce to request
    ACK = 3 # acknowledgement that data has been transmitted