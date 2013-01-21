import utils

def getAckPacket(number, acknumber):
	'''
	PAYLOAD		[ ACKNUMBER (64 bit) ]
	'''
	payload = utils.putLong(b"", acknumber)
	return Packet(Packet.TYPE_CONTROL, Packet.SUBTYPE_AGENT_AGENT_ACK, number, payload)

def getAckData(pack):
	return utils.getLong(pack.payload)
	
	
def getNackPacket(number, nacknumber):
	'''
	PAYLOAD		[ ACKNUMBER (64 bit) ]
	'''
	payload = utils.putLong(b"", nacknumber)
	return Packet(Packet.TYPE_CONTROL, Packet.SUBTYPE_AGENT_AGENT_NACK, number, payload)

def getNackData(pack):
	return utils.getLong(pack.payload)


def getHostServerRegisterPacket(number, hostname, service):
	'''
	PAYLOAD		[ HOSTNAME (64 Byte) | SERVICENAME (64 Byte) ]
	'''	
	if len(hostname) > 32:
		raise ValueError("hostname must be 32 characters or less")
	if len(service) > 32:
		raise ValueError("service must be 32 characters or less")
	hname = utils.putText(b"", hostname, 64)
	serv = utils.putText(b"", service, 64)
	payload = hname + serv
	return Packet(Packet.TYPE_CONTROL, Packet.SUBTYPE_HOST_SERVER_REGISTER, number, payload)

def getHostServerRegisterData(pack):
	return utils.getText(pack.payload, 64), utils.getText(pack.payload[64:], 64)


def getPacket(byteString):
	print repr(byteString)
	maintype = utils.getByte(byteString, Packet.POS_TYPE)
	subtype = utils.getByte(byteString, Packet.POS_SUBTYPE)
	number = utils.getLong(byteString, Packet.POS_SEQ_NR)
	return Packet(maintype, subtype, number, byteString[Packet.HEADER_LENGTH:])

class Packet:
	'''
	HEADER		[ TYPE (8 bit) | SUBTYPE (8 bit) |	SEQ_NUMBER (64 bit)	]
	'''

	POS_TYPE 	= (0, 1)
	POS_SUBTYPE = (1, 2)
	POS_SEQ_NR 	= (2, 10)

	PACKET_SIZE		= 512
	HEADER_LENGTH 	= 10
	PAYLOAD_SIZE	= PACKET_SIZE - HEADER_LENGTH
	
	TYPE_CONTROL	= 1
	TYPE_DATA		= 2
	
	SUBTYPE_HOST_SERVER_REGISTER	= 1		# registration as host of specific service at server
	SUBTYPE_HOST_SERVER_RDY			= 4		# socket created and ready to receive client addr
	
	SUBTYPE_CLIENT_SERVER_REQ_HOST 	= 2		# client request host address for specific service
	
	SUBTYPE_SERVER_HOST_OPEN		= 3		# open new socket and contact server through that port
	SUBTYPE_SERVER_AGENT_CONNECT 	= 5		# server sends address of host to client and addr of client to host
		
	SUBTYPE_AGENT_AGENT_ACK			= 6		# ack packet
	SUBTYPE_AGENT_AGENT_NACK		= 7		# noack packet
	SUBTYPE_AGENT_AGENT_ERROR		= 8
	SUBTYPE_AGENT_AGENT_PROBING		= 9		# client and host try to reach one another
	SUBTYPE_AGENT_AGENT_SUCCESS		= 10	# agent has successfully received other agents packet
	

	def __init__(self, maintype, subtype, number, payload):
		self.maintype = maintype
		self.subtype = subtype
		self.number = number
		self.payload = payload
		
	def __repr__(self):
		return str(self.maintype) + " " + str(self.subtype) + " " + str(self.number)

	def toByteArray(self):
		ret = b""
		ret = utils.putByte(ret, self.maintype)
		ret = utils.putByte(ret, self.subtype)
		ret = utils.putLong(ret, self.number)
		return ret + self.payload

			
class PacketError(Exception):
	
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return self.msg