from ast import Str
from distutils.text_file import TextFile
from http import server
from io import BufferedWriter, TextIOWrapper
from client import genericRequestBuilder
from headerEnums import MessageType
from packet_class import Packet, packetBuilder
from methods import calcPacketSize, multiPacketHandle, messageBuilder, multiSendPacket
from constants import bf_Size, hr_Size

import socket
import os

bufferSize = bf_Size
headerSize = hr_Size
serverSocket:socket.socket
txtfiles:str

def serverStart(hostAddress):
    global bufferSize
    global headerSize
    global serverSocket
    global txtfiles


    # * Socket Binding to host IP & Port 
    hostIP = hostAddress[0]
    hostPort = hostAddress[1]

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((hostIP, hostPort))

    print("\nUDP Server up! \nServerIP: ", str(hostIP),"\nServerPort: ", str(hostPort), "\nBuffer Size: ", str(bufferSize),"\n")

    txtfiles = fileReadIn()
    print("server done")
    # -------------------------------------------------------

    while True:
        #? instead of waiting for an initialHandshake at the start a method that handles requests should be written
        #initialHandshakeServer()

        #? check if this is possible so client is able to see list of files on connection???
        # packet = packetBuilder( serverSocket.recvfrom(bufferSize))
        # printFilesList(packet)

        handler()

def handler():
    packet = packetBuilder( serverSocket.recvfrom(bufferSize))
    print(packet.encodedHeader)
    if (packet.type == 1): #-request
        fileRequest(packet)
    elif (packet.type == 3):
        printFilesList(packet)
    else:
        print("!!ERROR UNKNOWN HEADER REQUEST TYPE!!")
    
def fileReadIn()-> str:
    txtfiles = ""
    files = os.listdir('./resources') # <- this is now a list of files
    ctr = 1
    for x in files:
        txtfiles = str(ctr) + " - " + x + ", \n" + txtfiles
        ctr = ctr + 1
    txtfiles = txtfiles + "\nWhich text file would you like to see?"
    return txtfiles

def fileRequest(packet: Packet):
    files = os.listdir('./resources')
    try:
        reqFileName = files[packet.req-1]
        fileLocation = "./resources/"+reqFileName
        IOwrapperFile = open(fileLocation, "r")
        file = IOwrapperFile.read()
    except:
        return ("!!File does not exist!!")

    multiSendPacket(Packet(MessageType.RES, 1, calcPacketSize(bufferSize - headerSize, file), 0, 0, packet.req, str(file).encode('utf-8'), packet.ip, packet.port), serverSocket, bufferSize)


def printFilesList(packet: Packet): 
    multiSendPacket(Packet(MessageType.GIV, 1, calcPacketSize(bufferSize - headerSize, txtfiles), 0, 0, 0, str(txtfiles).encode('utf-8'), packet.ip, packet.port), serverSocket, bufferSize)

