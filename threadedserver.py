import socket
import threading

std_ID = 13321463

class Server(object):

	max_workers = 16

	def __init__(self, host, port):
		#bind to port and host specified
		self.host = host
		self.port = port
		self.socket = socket.socket()
		self.socket.bind((self.host, self.port))
		#create task list and initialise the number of workers
		self.tasks = []
		self.no_of_workers = 0
		self.lock = Lock()


	def listen(self):
		self.socket.listen()
		while True:
			client, address = self.socket.accept()
			#add connection to task list
			self.tasks.append((client, address))
			#if we aren't at max threads and there are a few tasks waiting in the queue start another worker
			self.lock.acquire()
			if(self.no_of_workers < self.max_workers && len(tasks) > 3):
				self.no_of_workers +=1
				threading.Thread(target = self.Worker).start()
			self.lock.release()

	def Worker(self):
		while len(tasks) > 0:
			(client, (host, port)) = tasks.pop(0)
			size = 1024
	        while True:
	            try:
	                data = client.recv(size)
	                if data:
	                	data = data.decode("utf-8")
	                    # Set the response to echo back the recieved data 
	                    if data == "HELO text\n":
	                    	response = "HELO text\nIP:{0}\nPort:{1}\nStudentID:{2}\n".format(host, port, std_ID)
	                    else:
	                    	response = data
	                    client.send(response.encode("utf-8"))
	                else:
	                    raise error('Client disconnected')
	            except:
	                client.close()
	                return False