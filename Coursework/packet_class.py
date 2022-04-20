from email.message import Message
from typing import Tuple
from headerEnums import MessageType
from constants import hr_Size

class Packet:
  def __init__(self, type: MessageType, packetTot:int, packetData:bytes, address: str, port: int):
    
    #* [ packet1 = packet(...) ] <-- creating a packet object \
    self.type = type.value
    self.currentPacket = 1
    self.packetTot = packetTot
    self.checkSum = 0
    self.extra = 0

    self.encodedHeader = (self.type.to_bytes(1, 'little') 
    + self.currentPacket.to_bytes(1, 'little') 
    + self.packetTot.to_bytes(1, 'little') 
    + self.checkSum.to_bytes(1, 'little') 
    + self.extra.to_bytes(hr_Size-4, 'little'))

    self.packetData = packetData
    self.packet = self.encodedHeader + self.packetData
    self.ip = address
    self.port = port
    self.address = (address, port)

def packetBuilder(inPacket: Tuple)-> Packet: #! DO NOT TOUCH <- shove in message from socket and it will make an obj

  #- Header Format = Type | Cur Pack | Tot Pack | Check Sum | Extra 

  pData = inPacket[0]
  pAddress = inPacket[1]

  packetHeader = pData[:hr_Size]
  packetData = pData[hr_Size:]
  packetIP = pAddress[0]
  packetPort = pAddress[1]
  return(Packet(  MessageType(packetHeader[0]), packetHeader[2],  packetData,   packetIP, packetPort  ) )
