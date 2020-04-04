import socket
import threading
from src.server import core
from src.shared import stringify, logger

class Server():
	def __init__(self):
		super().__init__()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('0.0.0.0', 8080))
		self.socket.listen(5)

		self.core = core.Core()

	def on_update(self, dt, state):
		while True:
			self.core.on_update(dt, state)

	def receive(self, connection): 
		while True: 
			received = connection.recv(4096)
			if not received: break
			command_array = stringify.destringify(received)
			logger.log(f'Receiving {received.decode()}', logger.LOG_LEVEL_NETWORK)
			for command in command_array:
				command.data['connection'] = connection
				self.core.add_command(command)

	def run(self):
		self.update_thread = threading.Thread(target=lambda : self.on_update(None, None), daemon=True)
		self.update_thread.start()

		while True:
			connection, address = self.socket.accept()
			client_thread = threading.Thread(target=self.receive, args=(connection,), daemon=True)
			client_thread.start()
