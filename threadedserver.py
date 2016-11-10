import socket
import threading
import sys, argparse, os
from urllib.request import urlopen

std_ID = 13321463

class Server(object):

	max_workers = 16

	def __init__(self, host, port, ip):
		#bind to port and host specified
		self.host = host
		self.port = port
		self.socket = socket.socket()
		self.socket.bind((self.host, self.port))
		#create task list and initialise the number of workers
		self.tasks = []
		self.no_of_workers = 0
		self.lock = threading.Lock()
		self.ip = ip
		self.running = True

	def listen(self):
		self.socket.listen(5)
		while self.running:
			print("Waiting for connections")
			client, address = self.socket.accept()
			print("Received connection from {0}".format(address))
			#add connection to task list
			self.tasks.append((client, address))
			#if we aren't at max threads and there are a few tasks waiting in the queue start another worker
			self.lock.acquire()
			if(self.no_of_workers < self.max_workers and len(self.tasks) >= 0):
				print("Creating worker")
				self.no_of_workers +=1
				threading.Thread(target = self.Worker, daemon = True).start()
			self.lock.release()

	def Worker(self):
		print("Started worker. There are now {0} workers".format(self.no_of_workers))
		while len(self.tasks) > 0:
			(client, (host, port)) = self.tasks.pop(0)
			size = 1024
			while True:
				try:
					data = client.recv(size)
					data = data.decode("utf-8")
					if data is not "KILL_SERVICE\n":
						print("Received message: {0}".format(data))
						# Set the response to echo back the recieved data
						if data[0:5] == "HELO " and data[-1] == "\n":
							print("Adding student id.")
							response = "{3}IP:{0}\nPort:{1}\nStudentID:{2}\n".format(self.ip, self.port, std_ID, data)
							client.send(response.encode("utf-8"))
						elif data == "KILL_SERVICE\n":
							print("Calling Stop()")
							self.Stop()
						else:
							print("Handling other package.")
						print("Handled packet")
					else:
						raise error('Client disconnected')
				except:
					client.close()
					self.Stop()
					print("Got to break")
					break
		print("Worker dying")

	def Stop(self):
		self.running = False
		print("Running set to false")
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
		self.socket.close()
		sys.exit(1)

def clargs():
	parser = argparse.ArgumentParser(description='TCP thread pool server.')
	parser.add_argument('-p', '--port', type=int, required=True, help='Port to connect to')
	parser.add_argument('-o', '--host', required=False, help='Host name to send get request to')
	parser.add_argument('-i', '--ipAddress', required=True, help='IP address of host')
	return parser.parse_args()

if __name__ == '__main__':
	args = clargs()
	s = Server('', args.port, args.ipAddress)
	try:
		s.listen()
	except KeyboardInterrupt:
		print("Ctrl C - Stopping server")
		sys.exit(1)
	