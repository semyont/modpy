'''
Modbus Payload Decoders
------------------------

A collection of utilities for decoding
modbus messages payloads.
this version of the payload has custom extended decoders on top of the original + new long types
'''
from struct import pack, unpack
from pymodbus.constants import Endian
from pymodbus.utilities import pack_bitstring
from pymodbus.utilities import unpack_bitstring
from pymodbus.exceptions import ParameterException

BINARY_DECODERS = {
    '8bit_uint': 1,
    '16bit_uint': 2,
    '32bit_uint': 4,
    '32bit_ulong': 4,
    '64bit_uint': 8,
    '8bit_int': 1,
    '16bit_int': 2,
    '32bit_int': 4,
    '32bit_long': 4,
    '64bit_int': 8,
    '32bit_float': 4,
    '64bit_float': 8
}
EXTENDED_DECODERS = {
    'DWord_Modicon_Counter': 4,
    'Block_Extract': 19,
}


class BinaryPayloadDecoder(object):
    '''
    A utility that helps decode payload messages from a modbus
    reponse message.  It really is just a simple wrapper around
    the struct module, however it saves time looking up the format
    strings. What follows is a simple example::

        decoder = BinaryPayloadDecoder(payload)
        first   = decoder.decode_8bit_uint()
        second  = decoder.decode_16bit_uint()
    '''

    def __init__(self, payload, endian=Endian.Little):
        ''' Initialize a new payload decoder

        :param payload: The payload to decode with
        :param endian: The endianess of the payload
        '''
        self._payload = payload
        self._pointer = 0x00
        self._endian = endian

    @classmethod
    def fromRegisters(klass, registers, endian=Endian.Little):
        ''' Initialize a payload decoder with the result of
        reading a collection of registers from a modbus device.

        The registers are treated as a list of 2 byte values.
        We have to do this because of how the data has already
        been decoded by the rest of the library.

        :param registers: The register results to initialize with
        :param endian: The endianess of the payload
        :returns: An initialized PayloadDecoder
        '''
        if isinstance(registers, list):  # repack into flat binary
            payload = ''.join(pack(endian + 'H', x) for x in registers)
            return klass(payload, endian)
        raise ParameterException('Invalid collection of registers supplied')

    @classmethod
    def fromCoils(klass, coils, endian=Endian.Little):
        ''' Initialize a payload decoder with the result of
        reading a collection of coils from a modbus device.

        The coils are treated as a list of bit(boolean) values.

        :param coils: The coil results to initialize with
        :param endian: The endianess of the payload
        :returns: An initialized PayloadDecoder
        '''
        if isinstance(coils, list):
            payload = pack_bitstring(coils)
            return klass(payload, endian)
        raise ParameterException('Invalid collection of coils supplied')

    def reset(self):
        ''' Reset the decoder pointer back to the start
        '''
        self._pointer = 0x00

    def decode_8bit_uint(self):
        ''' Decodes a 8 bit unsigned int from the buffer
        '''
        self._pointer += 1
        fstring = self._endian + 'B'
        handle = self._payload[self._pointer - 1:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_bits(self):
        ''' Decodes a byte worth of bits from the buffer
        '''
        self._pointer += 1
        fstring = self._endian + 'B'
        handle = self._payload[self._pointer - 1:self._pointer]
        return unpack_bitstring(handle)

    def decode_16bit_uint(self):
        ''' Decodes a 16 bit unsigned int from the buffer
        '''
        self._pointer += 2
        fstring = self._endian + 'H'
        handle = self._payload[self._pointer - 2:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_32bit_uint(self):
        ''' Decodes a 32 bit unsigned int from the buffer
        '''
        self._pointer += 4
        fstring = self._endian + 'I'
        handle = self._payload[self._pointer - 4:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_32bit_ulong(self):
        ''' Decodes a 32 bit unsigned long from the buffer
        '''
        self._pointer += 4
        fstring = self._endian + 'L'
        handle = self._payload[self._pointer - 4:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_64bit_uint(self):
        ''' Decodes a 64 bit unsigned int from the buffer
        '''
        self._pointer += 8
        fstring = self._endian + 'Q'
        handle = self._payload[self._pointer - 8:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_8bit_int(self):
        ''' Decodes a 8 bit signed int from the buffer
        '''
        self._pointer += 1
        fstring = self._endian + 'b'
        handle = self._payload[self._pointer - 1:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_16bit_int(self):
        ''' Decodes a 16 bit signed int from the buffer
        '''
        self._pointer += 2
        fstring = self._endian + 'h'
        handle = self._payload[self._pointer - 2:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_32bit_int(self):
        ''' Decodes a 32 bit signed int from the buffer
        '''
        self._pointer += 4
        fstring = self._endian + 'i'
        handle = self._payload[self._pointer - 4:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_32bit_long(self):
        ''' Decodes a 32 bit signed long from the buffer
        '''
        self._pointer += 4
        fstring = self._endian + 'l'
        handle = self._payload[self._pointer - 4:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_64bit_int(self):
        ''' Decodes a 64 bit signed int from the buffer
        '''
        self._pointer += 8
        fstring = self._endian + 'q'
        handle = self._payload[self._pointer - 8:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_32bit_float(self):
        ''' Decodes a 32 bit float from the buffer
        '''
        self._pointer += 4
        fstring = self._endian + 'f'
        handle = self._payload[self._pointer - 4:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_64bit_float(self):
        ''' Decodes a 64 bit float(double) from the buffer
        '''
        self._pointer += 8
        fstring = self._endian + 'd'
        handle = self._payload[self._pointer - 8:self._pointer]
        return unpack(fstring, handle)[0]

    def decode_string(self, size=1):
        ''' Decodes a string from the buffer
        :param size: The size of the string to decode
        '''
        self._pointer += size
        return self._payload[self._pointer - size:self._pointer]

class Payload_Extended(BinaryPayloadDecoder):
    pass

__all__ = ["BinaryPayloadDecoder","Payload_Extended"]
