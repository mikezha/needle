
import time
import threading

import utils
import packet

seq_number = 1;
expected_ack_number = 1

class ControlListener(threading.Thread):
	'''
	listens for incoming packets from the mediator
	'''

	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		
	def run(self):
		while True:
			pack, addr = sock.recvfrom(65535)
			if pack.maintype == packet.Packet.TYPE_CONTROL:
				if pack.subtype == packet.Packet.SUBTYPE_AGENT_AGENT_ACK:
					print "ack from server, seq_number:", pack.number
					ack_data = packet.getAckData(pack)
					if ack_data == expected_ack_number:
						print "ack number matches sequence number, ack_number:", ack_data
						seq_number = pack.number + 1
						print "seq number set to:", seq_number
					else:
						print "ack number does not match sequence number, ack:", ack_data, "expected:", expected_ack_number

if __name__ == "__main__":
	sock = utils.UDPSocket();
	
	clistener = ControlListener()
	clistener.start()
	
	while True:
		print "sending register packet"
		pack = packet.getHostServerRegisterPacket(seq_number, "test", "test") 
		sock.sendto(pack, ("127.0.0.1", 20000))
		expected_ack_number = seq_number
		time.sleep(10)
		


