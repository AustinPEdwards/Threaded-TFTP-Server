'''
Austin Edwards
CSCE360 Assignment3
Constructs 5 all 5 kinds of TFTP packet headers:
	opcode 	operation
	--------------------------
	 1		Read request (RRQ)
	 2		Write request (WRQ)
	 3 		Data (DATA)
	 4		Acknowledgment (ACK)
 	 5 		Error (ERROR)
'''

import struct


# OPCODE 1:	RETURNS RRQ PACKET
def build_rrq(filename, mode):
    opcode = 1
    return build_request_packet(filename, mode, opcode)


# OPCODE 2:	RETURNS WRQ PACKET
def build_wrq(filename, mode):
    opcode = 2
    return build_request_packet(filename, mode, opcode)


# OPCODE 3:	RETURNS DATA PACKET
def build_data(data, blockNum):
    opcode = 3
    return build_data_packet(data, blockNum, opcode)


# OPCODE 4:	RETURNS ACK PACKET
def build_ack(blockNum):
    opcode = 4
    return build_ack_packet(opcode, blockNum)


# OPCODE 5:	RETURNS ERROR PACKET
def build_error(error_code, error_msg):
    opcode = 5
    return build_error_packet(error_code, error_msg, opcode)


# OPCODE: 1 OR 2	READ & WRITE REQUEST PACKET
def build_request_packet(filename, mode, opcode):
    if mode != 'netascii':
       raise Exception('mode is not \'netascii\'')
    packet = bytearray()
    filename = bytearray(filename.encode('utf-8'))
    mode = bytearray(mode.encode('utf-8'))
    # CREATE PACKET
    packet.append(0)		# byteArray: \x00
    packet.append(opcode)	# byteArray: \x00 \x'opcode'
    packet += filename		# byteArray: \x00 \x'opcode' 'filename'
    packet.append(0)		# byteArray: \x00 \x'opcode' 'filename' \x00
    packet += mode			# byteArray: \x00 \x'opcode' 'filename' \x00 'mode'
    packet.append(0)		# byteArray: \x00 \x'opcode' 'filename' \x00 'mode' \x00
    if len(packet) > 516:
        raise Exception('packet is too large (>516 bytes)')
    return packet


# OPCODE: 3			DATA PACKET
def build_data_packet(data, blockNum, opcode):
    if len(data) > 512:
        raise Exception('data is too large (>512 bytes)')
    packet = bytearray()
    data_length = str(len(data))
    format_string = '!HH' + data_length + 's'
    # CREATE PACKET
    packet = struct.pack(format_string, opcode, blockNum, data)	# byteArray: \x00 \x03 \(block number within 2 bytes) 'Data provided'
    return packet


# OPCODE: 4			ACKNOWLEDGEMENT PACKET
def build_ack_packet(opcode, blockNum):
    packet = bytearray()
    blockNum = blockNum.to_bytes(2,'big')
    # CREATE PACKET
    packet.append(0)						# byteArray: \x00
    packet.append(opcode)					# byteArray: \x00 \x'opcode'
    packet += blockNum						# byteArray: \x00 \x'opcode' \(block number within 2 bytes)
    return packet


# OPCODE: 5			ERROR PACKET
def build_error_packet(error_code, error_msg, opcode):
    if error_code > 7 or error_code < 0:
        raise Exception
    packet = bytearray()
    error_msg = bytearray(error_msg.encode('utf-8'))
    # CREATE PACKET
    packet.append(0)						# byteArray: \x00
    packet.append(opcode)					# byteArray: \x00 \x'opcode'
    packet.append(0)						# byteArray: \x00 \x'opcode' \x00
    packet.append(error_code)				# byteArray: \x00 \x'opcode' \x00 \x'error code
    packet += error_msg						# byteArray: \x00 \x'opcode' \x00 \x'error code 'error message'
    packet.append(0)						# byteArray: \x00 \x'opcode' \x00 \x'error code 'error message' \x00
    if len(packet) > 516:
        raise Exception('packet is too large (>516 bytes)')
    return packet




