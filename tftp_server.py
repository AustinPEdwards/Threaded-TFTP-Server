'''
Austin Edwards
CSCE360 Assignment3
File acts as a Threaded Trivial File Transfer Protocol Server using UDP.  Does basic read and write operations and handels errors
'''

import argparse
import socket
import os.path
import time
import threading
from constructpacket import build_rrq
from constructpacket import build_wrq
from constructpacket import build_data
from constructpacket import build_ack
from constructpacket import build_error

from deconstructpacket import unpack_data
from deconstructpacket import unpack_ack
from deconstructpacket import unpack_request_packet
from deconstructpacket import unpack_error


parser = argparse.ArgumentParser(description='Communicate Via TFTP')
parser.add_argument('-sp', '--serverport', type=int, help='Server Port', required=True)
args = parser.parse_args()
if (args.serverport < 5000 or args.serverport > 65535):
    print("Port numbers must be between 5000 and 65,535")
    exit()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', args.serverport))


# FUNCTION TO SEND A PACKET THAT HAS AN EXPECTED RESPONSE (RRQ, WRQ, DATA, or ACK)
def send_receive_packet(Socket, packet, clientAddressPort):
    # SEND PACKET
    Socket.sendto(packet, clientAddressPort)
    # LISTEN FOR A RESPONSE
    message, receivedAddressPort = Socket.recvfrom(2048)
    if message[1] == 5:
        return 'error'
    # CHECK FOR TID MATCH AND ERROR PACKET
    #message = check_tid(Socket, message, clientAddressPort, receivedAddressPort)
    # WHILE( PACKET IS EITHER A DATA OR ACK PACKET ) && (THE BLOCK NUMBERS FROM SENT AND RECEIVED PACKETS DO NOT MATCH)
    # BASICALLY CHECKS FOR DROPPED PACKETS AND RESENDS
    while (packet[1] == 3 and (message[2], message[3]) != (packet[2], packet[3])) \
       or (packet[1] == 4 and (int.from_bytes((message[2], message[3]), "big") != int.from_bytes((packet[2], packet[3]), "big") + 1)):
        # IF BLOCK NUMBER = 65535, START AT BLOCK NUMBER = 0
        if int.from_bytes((packet[2], packet[3]), "big") == 65535 and int.from_bytes((message[2], message[3]), "big") == 0:
            return (message)
        # RESEND LOST PACKET
        Socket.sendto(packet, clientAddressPort)
        # LISTEN FOR A RESPONSE
        message, receivedAddressPort = Socket.recvfrom(2048)
        # CHECK FOR TID MATCH AND ERROR PACKET
        #message = check_tid(Socket, message, clientAddressPort, receivedAddressPort)
    return(message)


def serverRead(filename, clientAddressPort):
    threadSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    threadSocket.bind(('', args.serverport))
    threadSocket.connect(clientAddressPort)
    threadSocket.settimeout(1)
    # CHECK IF PACKET IS ACK PACKET
    dataLen = 512
    blockNum = 1
    with open(filename, "r") as file_object:
        while dataLen == 512:
            # INCREASE BLOCK NUMBER BY 1 (STARTING AT 1)
            # COLLECT UP TO 512 BYTES OF DATA FROM FILE
            data = file_object.read(512)
            # RECORD DATA LENGTH
            dataLen = len(data)
            # CONVERT TO BYTE ARRAY
            data = bytearray(data.encode('utf-8'))
            # CONSTRUCT DATA PACKET
            packetDATA = build_data(data, blockNum)
            # SEND DATA PACKET
            message = send_receive_packet(threadSocket, packetDATA, clientAddressPort)
            # if the packet received is an error packet, exit thread gracefully
            if message == 'error':
                threadSocket.close()
                return
            # UNPACK ACK PACKET
            blockNum = unpack_ack(message)
            blockNum = blockNum + 1
    threadSocket.close()


def serverWrite(filename, clientAddressPort):
    threadSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    threadSocket.bind(('', args.serverport))
    threadSocket.connect(clientAddressPort)
    threadSocket.settimeout(1)
    filename = os.path.basename(filename)
    packetACK = build_ack(0)
    message = send_receive_packet(threadSocket, packetACK, clientAddressPort)
    # CHECK IF MESSAGE IS DATA PACKET
    if message[1] == 3:
        # UNPACK DATA PACKET
        (opcode, blockNum, data) = unpack_data(filename, message)
        # BUILD ACK PACKET
        packetACK = build_ack(blockNum)
        # IF DATA == 512, SEND ACK AND RECEIVE....
        if len(data) == 512:
            while len(data) > 511:
                # SEND ACK, RECEIVE DATA
                message = send_receive_packet(threadSocket, packetACK, clientAddressPort)
                # if the packet received is an error packet, exit thread gracefully
                if message == 'error':
                    threadSocket.close()
                    return
                # UNPACK DATA PACKET
                (opcode, blockNum, data) = unpack_data(filename, message)
                # BUILD ACK PACKET
                packetACK = build_ack(blockNum)

        # IF DATA < 512, SEND ACK AND SHUTDOWN CONNECTION
        # SEND FINAL ACK
        threadSocket.sendto(packetACK, clientAddressPort)
        threadSocket.close()


if __name__ == '__main__':
    start = True
    threads = []
    while start:
        message, clientAddressPort = serverSocket.recvfrom(2048)
        (opcode, filename, mode) = unpack_request_packet(message)

        if opcode == 1:     # client requesting to read
            if filename.endswith("shutdown.txt"):
                for t in threads:
                    t.join()
                serverSocket.close()
                exit()
            print("Starting thread")                    
            print("CLIENT: " + str(clientAddressPort))
            threads.append(threading.Thread(target=serverRead, args=(filename, clientAddressPort)))
            threads[len(threads)-1].start()

        elif opcode == 2:   # client requesting to write
            print("Starting thread")
            print("CLIENT: " + str(clientAddressPort))
            threads.append(threading.Thread(target=serverWrite, args=(filename, clientAddressPort)))
            threads[len(threads) - 1].start()
          
        elif opcode != 5:   # if the client receives a "non-error" packet from the wrong TID, send error packet
            errorPacket = build_error(5, 'Unknown transfer ID.')
            serverSocket.sendto(errorPacket, clientAddressPort)

        # if server receives an error packet from an unknown TID, do nothing

