from packet_class import Packet

def buildPacketChecksum(packet:Packet)->bytes:  # using the packet object this helper method will create a temp packet that does not 
                                                # hold the checksum to be used to calculate the recieved slice's checksum
    encodedHeader = ((0).to_bytes(4, 'little')
    + packet.type.to_bytes(1, 'little')
    + packet.sliceIndex.to_bytes(4, 'little') 
    + packet.lastSliceIndex.to_bytes(4, 'little') 
    + packet.fileIndex.to_bytes(4, 'little')
    + packet.bodyLength.to_bytes(2, 'little'))

    return encodedHeader+packet.packetData

def checkChecksum(packet:Packet)->bool: # returns a bool if checksum's given from slice and packet are the same

    givenChecksum = packet.checkSum
    calculatedChecksum = calcChecksum(buildPacketChecksum(packet))

    # print ("\n[checkChecksum] incoming packet       - ", packet.packet)
    # print ("[checkChecksum] checksum w/out checksum - ", buildPacketChecksum(packet))

    # print("\n[checkChecksum] header checksum - ", givenChecksum)
    # print("[checkChecksum] server calculated - ", calculatedChecksum)

    return (givenChecksum == calculatedChecksum)

def calcChecksum(data:bytes)->int: # algorithm used to calculate the checksum

    # print ("\n[calcChecksum] input bytes - ", str(data))

    x = 0
    for byte in data:
        x = (x + byte) & 0xFFFFFFFF
    return (((x ^ 0xFFFFFFFF) +1) & 0xFFFFFFFF)
