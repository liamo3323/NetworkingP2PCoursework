from ast import Bytes
from email.message import Message
from typing import Tuple
from headerEnums import MessageType
from constants import hr_Size

class Packet: # constructor method which will create a packet object
  #def __init__(self, type: MessageType, packetSliceIndex:int, packetLastSliceIndex:int, packetCheck:int, pacBodyLength:int, packetFileIndex:int, packetData:bytes, ip: str, port: int):
  def __init__(self, type: MessageType, packetLastSliceIndex:int, packetData:bytes, ip: str, port: int, packetFileIndex:int = 0, packetSliceIndex:int = 1, packetCheck:int = 0, pacBodyLength:int =0):
  
  # ! list of variables that should have default values: packetSliceIndex, packetCheck pacBodyLength, PacketFileIndex,

    #* Checksum - The calculation to check message integrity using longitudinal redundancy check. MUST be included.
    #* Message Type - Each communication MUST include one of the type options
    #* Slice index - is used to declare for the client which slice it wants to retrieve.
    #* Last slice index - The last slice index for a given file index
    #* File Index - index of the resource the client tries to obtain.
    #* Body length - size of the slice
    #* Body - contains the slice

    # it will instantialize the packet variables into the object with the help of default values
    self.checkSum = packetCheck
    self.type = type.value
    self.sliceIndex = packetSliceIndex
    self.lastSliceIndex = packetLastSliceIndex
    self.fileIndex = packetFileIndex
    self.bodyLength = pacBodyLength

    # ? ORDER OF HEADER: checksum > message type > slice index > last slice index > file index > body  length > Body...
    self.encodedHeader = (self.checkSum.to_bytes(4, 'little')
    + self.type.to_bytes(1, 'little')
    + self.sliceIndex.to_bytes(4, 'little') 
    + self.lastSliceIndex.to_bytes(4, 'little') 
    + self.fileIndex.to_bytes(4, 'little')
    + self.bodyLength.to_bytes(2, 'little'))

    self.packetData = packetData
    self.packet = self.encodedHeader + self.packetData
    self.ip = ip
    self.port = port
    self.address = (ip, port)

def packetBuilder(inPacket: Tuple)-> Packet:

    # ? ORDER OF HEADER: checksum > message type > slice index > last slice index > file index > body  length > Body...

    # after listening to a socket, this helper method will create a new packet object for ease of use.
    pData           = inPacket[0]
    pAddress        = inPacket[1]

    packetHeader    = pData[:hr_Size]
    packetData      = pData[hr_Size:]

    pacCheck        = int.from_bytes(packetHeader[0:4], 'little')
    pacType         = packetHeader[4] 
    pacSliceIdx     = int.from_bytes(packetHeader[5:9], 'little')
    pacFinSliceIdx  = int.from_bytes(packetHeader[9:13], 'little')
    pacFileIdx      = int.from_bytes(packetHeader[13:17], 'little')
    pacBodyLength   = int.from_bytes(packetHeader[17:19], 'little')

    packetIP        = pAddress[0]
    packetPort      = pAddress[1]
    return(Packet( MessageType(pacType), pacFinSliceIdx,   packetData,   packetIP, packetPort, packetSliceIndex=pacSliceIdx, packetCheck=pacCheck, pacBodyLength = pacBodyLength, packetFileIndex = pacFileIdx,) )


def objToPacket(packet:Packet) -> bytes: # after manipulating the packet object, the slice has to be recreated from the object
    encodedHeader = (packet.checkSum.to_bytes(4, 'little')
    + packet.type.to_bytes(1, 'little')
    + packet.sliceIndex.to_bytes(4, 'little') 
    + packet.lastSliceIndex.to_bytes(4, 'little') 
    + packet.fileIndex.to_bytes(4, 'little')
    + packet.bodyLength.to_bytes(2, 'little'))

    fullPacket = encodedHeader+packet.packetData
    return fullPacket
