from src.shared import stringify, logger

def send(command, socket):
	string_command = stringify.stringify(command)
	logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
	socket.send(string_command)

def update_and_send(command, data):
	command.data.update(data)
	command.data['connection'].send(stringify.stringify(command))

def create_and_send(command_type, data):
	command = Command(command_type, data)
	data['connection'].send(stringify.stringify(command))

class Command():
	def __init__(self, command_type, data={}):
		self.type = command_type
		self.data = data
