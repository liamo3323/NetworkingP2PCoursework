from email.message import Message
from typing import Tuple
from headerEnums import MessageType
from constants import hr_Size

class Packet:
  def __init__(self, type: MessageType, packetTot:int, packetData:bytes, ip: str, port: int):
    
    #* [ packet1 = packet(...) ] <-- creating a packet object \
    self.type = type.value
    self.currentPacket = 1
    self.packetTot = packetTot
    self.checkSum = 0
    self.headCheckSum = 0
    self.fileReqID = 0

    self.encodedHeader = (self.type.to_bytes(1, 'little') 
    + self.currentPacket.to_bytes(4, 'little') 
    + self.packetTot.to_bytes(4, 'little') 
    + self.checkSum.to_bytes(4, 'little') 
    + self.headCheckSum.to_bytes(4, 'little')
    + self.fileReqID.to_bytes(2, 'little'))

    self.packetData = packetData
    self.packet = self.encodedHeader + self.packetData
    self.ip = ip
    self.port = port
    self.address = (ip, port)

def packetBuilder(inPacket: Tuple)-> Packet: #! DO NOT TOUCH <- shove in message from socket and it will make an obj

  #- Header Format = Type | Cur Pack | Tot Pack | Check Sum | Extra 

  pData = inPacket[0]
  pAddress = inPacket[1]

  packetHeader = pData[:hr_Size]
  packetData = pData[hr_Size:]

  pacType = packetHeader[0]
  pacCur = int.from_bytes(packetHeader[1:5], 'little')
  pacTot = int.from_bytes(packetHeader[5:9], 'little')
  pacCheck = int.from_bytes(packetHeader[9:13], 'little')
  pacHeadCheck = int.from_bytes(packetHeader[13:17], 'little')
  pacReq = int.from_bytes(packetHeader[17:19], 'little')

  print(pacType)
  packetIP = pAddress[0]
  packetPort = pAddress[1]
  return(Packet(  MessageType(pacType), pacTot,  packetData,   packetIP, packetPort  ) )
