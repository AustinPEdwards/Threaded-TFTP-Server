'''
Austin Edwards
CSCE360 Assignment3
pytest for constructing and deconstructing packets
'''
import constructpacket
import deconstructpacket
import pytest

########################################################################################################################################
#
#   TESTING CREATING PACKETS FROM constructpacket.py
#
########################################################################################################################################
# TESTING: CREATING RRQ PACKETS
# VALID TESTS
@pytest.mark.parametrize('filename, mode, expected', [
    ('test\for\building\rrq\packet.txt',  'netascii', bytearray(b'\x00\x01test\for\building\rrq\packet.txt\x00netascii\x00')),
    ('test\for\building\rrq\packet',  'netascii', bytearray(b'\x00\x01test\for\building\rrq\packet\x00netascii\x00'))])
def test_valid_build_rrq(filename, mode, expected):
    # byteArray: \x00 \x01 'filename' \x00 'mode' \x00
    assert constructpacket.build_rrq(filename, mode) == expected

# INVALID TESTS: PACKET > 516 BYTES,  MODE NOT 'netascii'
@pytest.mark.parametrize('filename, mode', [
    ('test\for\too\large\filename\012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890',  'netascii'),
     ('test\for\incorrect\mode',  'not_netascii')])
def test_invalid_build_rrq(filename, mode):
    with pytest.raises(Exception):
        constructpacket.build_rrq(filename, mode)


########################################################################################################################################
# TESTING: CREATING WRQ PACKETS
# VALID TESTS
@pytest.mark.parametrize('filename, mode, expected', [
    ('test\for\building\wrq\packet.txt',  'netascii', bytearray(b'\x00\x02test\for\building\wrq\packet.txt\x00netascii\x00')),
    ('test\for\building\wrq\packet',  'netascii', bytearray(b'\x00\x02test\for\building\wrq\packet\x00netascii\x00'))])
def test_valid_build_wrq(filename, mode, expected):
    # byteArray: \x00 \x02 'filename' \x00 'mode' \x00
    assert constructpacket.build_wrq(filename, mode) == expected

# INVALID TESTS: PACKET > 516 BYTES,  MODE NOT 'netascii'
@pytest.mark.parametrize('filename, mode', [
    ('test\for\too\large\filename\012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890',  'netascii'),
     ('test\for\incorrect\mode',  'not_netascii')])
def test_invalid_build_wrq(filename, mode):
    with pytest.raises(Exception):
        constructpacket.build_wrq(filename, mode)


########################################################################################################################################
# TESTING: CREATING DATA PACKETS
# VALID TESTS
@pytest.mark.parametrize('data, blockNum, expected', [
    (bytearray(('').encode('utf-8')),  1, bytearray(b'\x00\x03\x00\x01')),
    (bytearray(('ThisIsSomeDataIWantToSend').encode('utf-8')),  255, bytearray(b'\x00\x03\x00\xffThisIsSomeDataIWantToSend')),
    (bytearray(('ThisIsSomeDataIWantToSend').encode('utf-8')),  65535, bytearray(b'\x00\x03\xff\xffThisIsSomeDataIWantToSend'))])
def test_valid_build_data(data, blockNum, expected):
    # byteArray: \x00 \x03 \(block number within 2 bytes) 'Data provided'
    assert constructpacket.build_data(data, blockNum) == expected

# INVALID TESTS: DATA > 512 BYTES
@pytest.mark.parametrize('data, blockNum', [
    (bytearray(('test\for\too\large\filename\012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890').encode('utf-8')),  1)])
def test_invalid_build_data(data, blockNum):
    with pytest.raises(Exception):
        constructpacket.build_data(data, blockNum)


########################################################################################################################################
# TESTING: CREATING ACK PACKETS
# VALID TESTS
@pytest.mark.parametrize('blockNum, expected', [
    (1, bytearray(b'\x00\x04\x00\x01')),
    (255, bytearray(b'\x00\x04\x00\xff')),
    (65535, bytearray(b'\x00\x04\xff\xff'))])
def test_valid_build_ack(blockNum, expected):
    # byteArray: \x00 \x'opcode' \(block number within 2 bytes)
    assert constructpacket.build_ack(blockNum) == expected


########################################################################################################################################
# TESTING: CREATING ERROR PACKETS
# VALID TESTS
@pytest.mark.parametrize('errorCode, errorMsg, expected', [
    (0, 'Not defined, see error message (if any).', bytearray(b'\x00\x05\x00\x00Not defined, see error message (if any).\x00')),
    (5, 'Unknown transfer ID.', bytearray(b'\x00\x05\x00\x05Unknown transfer ID.\x00')),
    (7, 'No such user.', bytearray(b'\x00\x05\x00\x07No such user.\x00'))])
def test_valid_build_error(errorCode, errorMsg, expected):
    # byteArray: \x00 \x'opcode' \x00 \x'error code 'error message' \x00
    assert constructpacket.build_error(errorCode, errorMsg) == expected

# INVALID TESTS: DATA > 512 BYTES
@pytest.mark.parametrize('errorCode, errorMsg', [
    (8, 'invalid Error Code'),
    (0, 'TestForTooLargeErrorMessage\012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890')])
def test_invalid_build_error(errorCode, errorMsg):
    with pytest.raises(Exception):
        constructpacket.build_error(errorCode, errorMsg)


########################################################################################################################################
#
#   TESTING UNPACKING PACKETS FROM deconstructpacket.py
#
########################################################################################################################################
# TESTING: UNPACKING REQUEST PACKETS, RRQ OR WRQ
# VALID TESTS
@pytest.mark.parametrize('packet, opcode, filename, mode', [
    (bytearray(b'\x00\x01test\for\building\rrq\packet.txt\x00netascii\x00'), 1, 'test\for\building\rrq\packet.txt', 'netascii'),
    (bytearray(b'\x00\x02test\for\building\wrq\packet.txt\x00netascii\x00'), 2, 'test\for\building\wrq\packet.txt', 'netascii'),
    (bytearray(b'\x00\x01test\for\building\rrq\packet\x00netascii\x00'), 1, 'test\for\building\rrq\packet', 'netascii')])
def test_valid_unpack_request_packet(packet, opcode, filename, mode):
    # byteArray: \x00 \x01 'filename' \x00 'mode' \x00
    assert deconstructpacket.unpack_request_packet(packet) == (opcode, filename, mode)

# INVALID TESTS: INVALID OPCODE, INVALID MODE, PACKET > 516 BYTES
@pytest.mark.parametrize('packet', [
    (bytearray(b'\x00\x03test\for\invalid\op\code\x00netascii\x00')),
    (bytearray(b'\x00\x02test\for\invalid\mode\x00not_netascii\x00')),
    (bytearray(b'\x00\x01TestForTooLargeErrorMessage\012345678901234567890123456789012345678901234567890123456789012345678901234567890 \
    1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890 \
    1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890 \
    1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890 \
    1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890 \
    123456789012345678901234567890x00netascii\x00'))])
def test_valid_unpack_request_packet(packet):
    with pytest.raises(Exception):
        deconstructpacket.unpack_request_packet(packet)


########################################################################################################################################
# TESTING: UNPACKING DATA PACKETS
@pytest.mark.parametrize('filename, packet, opcode, blockNum, data', [
    ('test.txt', bytearray(b'\x00\x03\x00\x01'), 3, 1, bytearray(''.encode('utf-8'))),
    ('test.txt', bytearray(b'\x00\x03\x00\xffThisIsSomeDataIAmReceiving'), 3, 255, bytearray('ThisIsSomeDataIAmReceiving'.encode('utf-8'))),
    ('test.txt', bytearray(b'\x00\x03\xff\xffThisIsSomeDataIAmReceiving'), 3, 65535, bytearray('ThisIsSomeDataIAmReceiving'.encode('utf-8')))])
def test_valid_unpack_data(filename, packet, opcode, blockNum, data):
    # byteArray: \x00 \x01 'filename' \x00 'mode' \x00
    assert deconstructpacket.unpack_data(filename, packet) == (opcode, blockNum, data)

# INVALID TESTS: DATA > 512 BYTES
@pytest.mark.parametrize('filename, packet', [
    ('test.txt', bytearray(('test\for\too\large\filename\012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890' 
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890').encode('utf-8')))])
def test_invalid_build_data(filename, packet):
    with pytest.raises(Exception):
        constructpacket.unpack_data(filename, packet)


        


