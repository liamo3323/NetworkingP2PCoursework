from headerEnums import MessageType
from constants import hr_Size

class Packet:
  def __init__(self, type: MessageType, packetNum:int, packetTot:int, packetData:bytes, address: str, port: int):
    
    #* [ packet1 = packet(...) ] <-- creating a packet object \

    self.type = type.value
    self.currentPacket = packetNum
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

def packetBuilder(inPacket:Packet): #! DO NOT TOUCH <- shove in message from socket and it will make an obj
  print("ejweja")
  packetHeader = (inPacket[0])[:6]
  packetData = (inPacket[0])[6:]
  packetAdd = inPacket[1]
  packetIP = packetAdd[0]
  packetPort = packetAdd[1]
  return(Packet(  MessageType(packetHeader[1]), packetHeader[2], packetHeader[3],  packetData,   packetIP, packetPort)  )
