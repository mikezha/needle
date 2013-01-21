
import sys
import time
import threading

import utils

remote_host = "pueh.at"
remote_port = 20000

expected_client_addr = None

class STATE:
	stage1 = False
	stage2 = False
	shutdown = False

def listen():
	while not STATE.shutdown:
		data, addr = sock.recvfrom(65535)
		if addr[0] == expected_client_addr[0]:				# has to be other client
			if not STATE.stage1:
				STATE.stage1 = True
			elif not STATE.stage2:
				if data == "success":
					STATE.stage2 = True
			else:
				print data
		

if __name__ == "__main__":
	sock = utils.UDPSocket()
	remote_addr = (remote_host, remote_port)
	
	
	print "socket created on", sock.getsockname()
	
	sock.sendto("test", remote_addr)
	data, addr = sock.recvfrom(65535)
	cl_addr = data.split("\n")
	print "client address:", cl_addr
	expected_client_addr = (cl_addr[0], int(cl_addr[1]))
	
	listen_thread = threading.Thread(target=listen)
	listen_thread.setDaemon(True)
	listen_thread.start()
	
	wait_time = 1
	while not STATE.stage1:
		print "sending connecting to remote client"
		sock.sendto("connecting", expected_client_addr)	
		time.sleep(wait_time)
		
	print "received packet from remote client"
		
	while not STATE.stage2:
		print "sending success to remote client"
		sock.sendto("success", expected_client_addr)
		time.sleep(wait_time)	
		
	print "tunnel stable to client at", expected_client_addr, "success"
	print "you can now type messages to the other client"
	
	while True:
		sock.sendto(raw_input(), expected_client_addr)
	
	print "exiting"
	
	STATE.shutdown = True
	sock.close()
	listen_thread.join()
	
	
	
	