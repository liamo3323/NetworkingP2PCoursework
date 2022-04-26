from packet_class import Packet

def buildPacketChecksum(packet:Packet)->bytes:
    encodedHeader = ((0).to_bytes(4, 'little')
    + packet.type.to_bytes(1, 'little')
    + packet.sliceIndex.to_bytes(4, 'little') 
    + packet.lastSliceIndex.to_bytes(4, 'little') 
    + packet.fileIndex.to_bytes(4, 'little')
    + packet.bodyLength.to_bytes(2, 'little'))

    return encodedHeader+packet.packetData

def checkChecksum(packet:Packet)->bool:

    givenChecksum = packet.checkSum
    calculatedChecksum = calcChecksum(buildPacketChecksum(packet))

    print ("given bytes     - ", packet.packet)
    print ("calcualtd bytes - ", buildPacketChecksum(packet))

    print("\n\ngiven     ", givenChecksum)
    print("calculated", calculatedChecksum)

    if (givenChecksum == calculatedChecksum):
        return True
    else:
        return False


def calcChecksum(data:bytes)->int:
    print ("calcchecksum input bytes - ")
    print(data)
    x = 0
    for byte in data:
        x = (x + byte) & 0xFFFFFFFF
    return (((x ^ 0xFFFFFFFF) +1) & 0xFFFFFFFF)
