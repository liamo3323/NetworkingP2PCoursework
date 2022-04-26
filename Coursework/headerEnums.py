from enum import Enum
class MessageType(Enum):
    REQ = 1 # requesting something
    RES = 2 # responce to request
    