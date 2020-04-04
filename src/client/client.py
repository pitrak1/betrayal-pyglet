import socket
import threading
from src.shared import stringify, node, logger

class Client(node.Node):
	def __init__(self, add_command):
		super().__init__()
		self.add_command = add_command
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect(('0.0.0.0', 8080))
		self.receive_thread = threading.Thread(target=self.receive, daemon=True)
		self.receive_thread.start()

	def receive(self):
		while True:
			received = self.socket.recv(4096)
			if not received: break
			logger.log(f'Receiving {received.decode()}', logger.LOG_LEVEL_NETWORK)
			command_array = stringify.destringify(received)
			for command in command_array:
				self.add_command(command)

	def network_create_player_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next(command.data['player_name'])
		elif command.data['status'] == 'invalid_player_name':
			state.invalid_player_name()
		elif command.data['status'] == 'name_too_short':
			state.name_too_short()
		elif command.data['status'] == 'name_too_long':
			state.name_too_long()

	def network_create_game_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next(command.data['game_name'])
		elif command.data['status'] == 'invalid_game_name':
			state.invalid_game_name()
		elif command.data['status'] == 'name_too_short':
			state.name_too_short()
		elif command.data['status'] == 'name_too_long':
			state.name_too_long()

	def network_leave_game_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.back()

	def network_get_players_in_game_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_players(command.data['players'])

	def network_get_games_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_games(command.data['games'])

	def network_join_game_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next(command.data['game_name'])
		elif command.data['status'] == 'game_full':
			state.game_full()

	def network_logout_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.exit()

	def network_start_game_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next()
		elif command.data['status'] == 'not_enough_players':
			state.not_enough_players()

	def network_get_player_order_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_player_order(command.data['players'])

	def network_confirm_player_order_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next()

	def network_get_available_characters_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_available_characters(command.data['characters'])

	def network_get_current_player_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_current_player(command.data['player_name'])

	def network_select_character_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)

	def network_all_characters_selected_handler(self, command, state=None):
		if command.data['status'] == 'success':
			state.next()

	def network_get_character_selections_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_character_selections(command.data['selections'])

	def network_confirm_character_selections_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.next()

	def network_get_player_positions_handler(self, command, state=None):
		if command.data['status'] == 'pending':
			string_command = stringify.stringify(command)
			logger.log(f'Sending {string_command.decode()}', logger.LOG_LEVEL_NETWORK)
			self.socket.send(string_command)
		elif command.data['status'] == 'success':
			state.set_player_positions(command.data['players'])
