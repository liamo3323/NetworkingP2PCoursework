from headerEnums import MessageType

class packet:
  def __init__(self, type: MessageType, packetTot:int, packetData:bytes, address:int, port:int):
    
    #* [ packet1 = packet(...) ] <-- creating a packet object \

    self.type = type.value
    self.currentPacket = 0
    self.packetTot = packetTot
    self.checkSum = 0
    self.extra = 0

    self.encodedHeader = (self.type.to_bytes(1, 'little') 
    + self.currentPacket.to_bytes(1, 'little') 
    + self.packetTot.to_bytes(1, 'little') 
    + self.checkSum.to_bytes(1, 'little') 
    + self.extra.to_bytes(HEADER-4, 'little'))

    self.packetData = packetData
    self.packet = self.encodedHeader + self.packetData
    self.address = address
    self.port = port

def getPacket(self):
    return self.packet

def getAddress(self):
    return self.address

def getPort(self):
    return self.port

def getType(self):
    return self.type

def getCurrentPacket(self):
    return self.currentPacket

def getPacketTotal(self):
    return self.packetTotal

def getCheckSum(self):
    return self.checkSum