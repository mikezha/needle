
import socket
import utils

local_port = 20000

hosts_by_service = {}

host_addr = None

if __name__ == "__main__":
	sock = utils.UDPSocket((utils.ALL_INTERFACES, local_port))
	
	print "socket created on", sock.getsockname()
	

	while True:
		data, addr = sock.recvfrom(65535)
		
		print "received", data, "from", addr
		
		if host_addr == None:
			host_addr = addr
			print "host set to", addr
			
		else:
			sock.sendto(str(host_addr[0]) + "\n" + str(host_addr[1]), addr)
			print "sent", str(host_addr[0]) + "\n" + str(host_addr[1]), "to", addr, "(client)"
			
			sock.sendto(str(addr[0]) + "\n" + str(addr[1]), host_addr)
			print "sent", str(addr[0]) + "\n" + str(addr[1]), "to", host_addr, "(host)"
			
			host_addr = None
	
	sock.close()
