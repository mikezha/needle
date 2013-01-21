import socket
import struct

import packet

ALL_INTERFACES = "";		#all interfaces
RANDOM_PORT = 0;			#let os pick port

class UDPSocket:

	def __init__(self, addr=(ALL_INTERFACES, RANDOM_PORT)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(addr)
		
	def getsockname(self):
		return self.sock.getsockname()
		
	def recvfrom(self, bytes):
		data, addr = self.sock.recvfrom(bytes)
		return packet.getPacket(data), addr
		
	def sendto(self, packet, addr):
		return self.sock.sendto(packet.toByteArray(), addr)
		
	def settimeout(self, seconds):
		return self.sock.settimeout(seconds)
		
	def close(self):
		return self.sock.close()
		
		
		
def putRawBytes(data, bytes, byteFormat, position=(-1, -1)):

	if len(position) != 2:
		raise ValueError("position must be a tuple or list of size 2")

	size = struct.calcsize(byteFormat)
	
	if position[0] < 0 or position[1] < 0:
		size = struct.calcsize(byteFormat)
		position=(len(data), len(data) + size)
		
	elif (position[1] - position[0]) != size:
		raise ValueError("position must define an interval of length " + str(size) + " when using format " + byteFormat)
	
	byteData = struct.pack(byteFormat, bytes)
	data = data[:position[0]] + byteData + data[position[1]:]
	return data
	

def getRawBytes(data, byteFormat, position):
	if len(position) != 2:
		raise ValueError("position must be a tuple or list of size 2")

	size = struct.calcsize(byteFormat)
	
	if position[0] < 0 or position[1] < 0:
		size = struct.calcsize(byteFormat)
		position=(0, size)
		
	elif (position[1] - position[0]) != size:
		raise ValueError("position must define an interval of length " + str(size) + " when using format " + byteFormat)
	
	return struct.unpack(byteFormat, data[position[0]:position[1]])[0]


	
def putByte(data, byteValue, position=(-1, -1)):
	return putRawBytes(data, byteValue, "!b", position)
		
def getByte(data, position=(-1, -1)):
	return getRawBytes(data, "!b", position)
	
def putChar(data, byteValue, position=(-1, -1)):
	return putRawBytes(data, byteValue, "!h", position)
		
def getChar(data, position=(-1, -1)):
	return getRawBytes(data, "!h", position)
	
def putInteger(data, integerValue, position=(-1, -1)):
	return putRawBytes(data, integerValue, "!i", position)
		
def getInteger(data, position=(-1, -1)):
	return getRawBytes(data, "!i", position)
	
def putLong(data, longValue, position=(-1, -1)):
	return putRawBytes(data, longValue, "!q", position)
		
def getLong(data, position=(-1, -1)):
	return getRawBytes(data, "!q", position)
	
def putText(data, text, bytelength=-1):
	padding = b""
	if bytelength != -1:
		if len(text)*2 > bytelength:
			raise ValueError("bytelength must be greater or equal to 2 * len(text)")
		else:
			padding = putByte(padding, 0) * (bytelength - 2*len(text))

	ret = b""
	for ch in text:
		ret = putChar(ret, ord(ch))
	ret = ret + padding
	
	return data + ret

		
def getText(data, maxbytelenght, start=0):
	internalPos = (start, start+2)	

	actualMaxPos = start + maxbytelenght
		
	text = ""
	while internalPos[1] < actualMaxPos:
		char = getChar(data, internalPos)
		if char == 0:
			break
		text = text + chr(char)
		internalPos = (internalPos[0] + 2, internalPos[1] + 2)
		
	return text
	
	
	
	
	
	
	
	
	