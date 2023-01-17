'''
Austin Edwards
CSCE360 Assignment3
Deconstructs 5 all 5 kinds of TFTP packet headers:
	opcode 	operation
	--------------------------
	 1		Read request (RRQ)
	 2		Write request (WRQ)
	 3 		Data (DATA)
	 4		Acknowledgment (ACK)
 	 5 		Error (ERROR)
'''


def unpack_request_packet(packet):
	packet = bytearray(packet)
	opcode = packet[1]
	filename = bytearray()
	mode = bytearray()

	if len(packet) > 516:
		raise Exception('packet is too large (>516 bytes)')
	if opcode != 1 and opcode != 2:
		raise Exception('Invalid Opcode for Request Packet')

	index = 2
	while packet[index] != 0:
		filename.append(packet[index])
		index += 1
	index += 1
	while packet[index] != 0:
		mode.append(packet[index])
		index += 1

	filename = filename.decode('utf-8')
	mode = mode.decode('utf-8')
	if mode != 'netascii':
		raise Exception('mode is not \'netascii\'')
	return opcode, filename, mode



# OPCODE: 3		DECONSTRUCTS DATA PACKET
def unpack_data(filename, packet):
	if len(packet) > 516:
		raise Exception('packet is too large (>516 bytes)')
	opcode = 3
	# GETS BLOCK NUMBER FROM BYTES 3 AND 4 of BYTEARRAY
	blockNum = int.from_bytes((packet[2],packet[3]), "big")
	# INITIALIZE DATA TO BYTEARRAY
	data = bytearray()
	# START INDEX AT 4 (0 AND 1 are OPCODE, 2 and 3 ARE BLOCK NUMBER)
	index = 4
	# IF LENGTH IS LESS THAN 5, THEN IT IS AN EMPTY DATA PACKET
	# SIGNIFIES END OF TRANSMISSION (IMPORTANT WHEN SENDING PRECISELY MAX DATA)
	if (len(packet) < 5):
		with open(filename,"ba") as file_object:
			# OPEN FILE, WRITE NOTHING AND CLOSE FILE
			file_object.close()
	# IF PACKET LENGTH IS OVER 4, PACKET HAS DATA
	else:
		# DO THIS WHILE INDEX IS SMALLER THAN THE PACKET LENGTH
		while (index < len(packet)):
			# STEP THROUGH PACKET AND APPEND TO DATA
			data.append(packet[index])
			index = index + 1
		# AFTER ALL DAT IS WRITTEN, WRITE DATA TO FILE
		with open(filename, "ba") as file_object:
			file_object.write(data)

		file_object.close()
	return opcode, blockNum, data


# OPCODE: 4		DECONSTRUCTS ACK PACKET
def unpack_ack(packet):
	opcode = 4
	# READ BYTES 3 AND 4 TO GET BLOCK NUMBER
	blockNum = int.from_bytes((packet[2], packet[3]), "big")
	return blockNum


# OPCODE: 4		DECONSTRUCTS ERROR PACKET
def unpack_error(packet):
	opcode = 5
	# ERROR CODE FOUND IN BYTE 4
	error_code = packet[3]
	# INITIALIZE ERROR MESSAGE TO BYTE ARRAY
	error_msg = bytearray()
	# START INDEX AT 4 (0 AND 1 are OPCODE, 2 IS 0, AND 3 IS ERROR CODE)
	index = 4
	# DO THIS WHILE INDEX IS SMALLER THAN THE PACKET LENGTH
	while index < len(packet):
		# STEP THROUGH PACKET AND APPEND TO DATA
		error_msg.append(packet[index])
		index = index + 1
	# DECODE ERROR MESSAGE
	error_msg = error_msg.decode('utf-8')
	return error_code, error_msg