from ast import Bytes
from email.message import Message
from typing import Tuple
from headerEnums import MessageType
from constants import hr_Size

class Packet:
  def __init__(self, type: MessageType, packetCur:int, packetTot:int, packetCheck:int, packetHeadCheck:int, packetReq:int, packetData:bytes, ip: str, port: int):
    
    #* [ packet1 = packet(...) ] <-- creating a packet object \
    self.type = type.value
    self.currentPacket = packetCur
    self.packetTot = packetTot
    self.checkSum = packetCheck
    self.headCheckSum = packetHeadCheck
    self.req = packetReq

    self.encodedHeader = (self.type.to_bytes(1, 'little') 
    + self.currentPacket.to_bytes(4, 'little') 
    + self.packetTot.to_bytes(4, 'little') 
    + self.checkSum.to_bytes(4, 'little') 
    + self.headCheckSum.to_bytes(4, 'little')
    + self.req.to_bytes(2, 'little'))

    self.packetData = packetData
    self.packet = self.encodedHeader + self.packetData
    self.ip = ip
    self.port = port
    self.address = (ip, port)

def packetBuilder(inPacket: Tuple)-> Packet:

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

	packetIP = pAddress[0]
	packetPort = pAddress[1]
	return(Packet(  MessageType(pacType), pacCur, pacTot, pacCheck, pacHeadCheck, pacReq,  packetData,   packetIP, packetPort  ) )

def objToPacket(packet:Packet) -> bytes:
	encodedHeader = (packet.type.to_bytes(1, 'little') 
    + packet.currentPacket.to_bytes(4, 'little') 
    + packet.packetTot.to_bytes(4, 'little') 
    + packet.checkSum.to_bytes(4, 'little') 
    + packet.headCheckSum.to_bytes(4, 'little')
    + packet.req.to_bytes(2, 'little'))
	fullPacket = encodedHeader+packet.packetData
	return fullPacket


def calcChecksum(data:bytes)->int:
    x = 0
    for byte in data:
        x = (x + byte) & 0xFFFFFFFF
    return (((x ^ 0xFFFFFFFF) +1) & 0xFFFFFFFF)
    

def checkChecksum(packet:Packet)->bool:
    givenChecksum = packet.checkSum
    calculatedChecksum = calcChecksum(buildPacketChecksum(packet))

    if (givenChecksum == calculatedChecksum):
        return True
    else:
        return False

def buildPacketChecksum(packet:Packet)->bytes:
    encodedHeader = (packet.type.to_bytes(1, 'little') 
    + packet.currentPacket.to_bytes(4, 'little') 
    + packet.packetTot.to_bytes(4, 'little') 
    + (0).to_bytes(4, 'little') 
    + packet.headCheckSum.to_bytes(4, 'little')
    + packet.req.to_bytes(2, 'little'))
    return encodedHeader+packet.packetData
