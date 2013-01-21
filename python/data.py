
import multiprocessing
import threading

import packet
import utils

class HostDataChannel(multiprocessing.Process):

	RECONNECT_RETRY_COUNT = 5		
	RECONNECT_RETRY_TIMEOUT = 30	#seconds

	def __init__(self, mediatorAddress, relayAddress):
		multiprocessing.Process.__init__(self)
		self.mediatorAddress = mediatorAddress
		self.relayAddress = relayAddress
		
	def run(self):
		try:
			udpSock = utils.UDPSocket()
		except socket.error as se:
			print "an error has occured while creating the socket:", repr(se)
			return
		
		udpSock.settimeout(HostDataChannel.RECONNECT_RETRY_TIMEOUT)
		
		tries = 0
		while True:
			
			if tries >= HostDataChannel.RECONNECT_RETRY_COUNT:
				print "maximum retries reached, connection to server lost, returning"
				return
			
			#send SUBTYPE_HOST_SERVER_RDY (subtype 4)
			
			try:
				pack, addr = udpSock.recvfrom(65535)
			except socket.timeout as to:
				tries = tries + 1
				continue
			except socket.error as se:
				print "an error has occured while listening for packets:", repr(se)
				
			
