from enum import Enum
from main import HEADER
class MessageType(Enum):
    h = 0 # initialHandshake
    r = 1 # request

def headerCreator(type: MessageType, packetTot: int) -> bytes:
    currentPacket = 0
    checkSum = 0
    extra = 0
    type = type.value

    encodedHeader = (type.to_bytes(1, 'little') 
    + currentPacket.to_bytes(1, 'little') 
    + packetTot.to_bytes(1, 'little') 
    + checkSum.to_bytes(1, 'little') 
    + extra.to_bytes(HEADER-4, 'little'))

    return encodedHeader