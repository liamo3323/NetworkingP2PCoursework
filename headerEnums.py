from enum import Enum
class MessageType(Enum): # different Enum types holding values which RFC state are  for different states in the protocol
    REQ = 1 # requesting something
    RES = 2 # responce to request
    fake = 3