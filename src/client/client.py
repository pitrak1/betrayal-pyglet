import socket
import threading
from src.shared import stringify, node, logger, command

class Client(node.Node):
	def __init__(self, add_command, testing=False):
		super().__init__()
		self.add_command = add_command
		self.testing = testing
		self.socket = None
		if not self.testing:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect(('0.0.0.0', 8080))
			self.receive_thread = threading.Thread(target=self.receive, daemon=True)
			self.receive_thread.start()

	def receive(self):
		if not self.testing:
			while True:
				received = self.socket.recv(4096)
				if not received: break
				logger.log(f'Receiving {received.decode()}', logger.LOG_LEVEL_NETWORK)
				command_array = stringify.destringify(received)
				for command_ in command_array:
					self.add_command(command_)

	def network_create_player_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next(command_.data['player_name'])
		elif command_.data['status'] == 'invalid_player_name':
			state.invalid_player_name()
		elif command_.data['status'] == 'name_too_short':
			state.name_too_short()
		elif command_.data['status'] == 'name_too_long':
			state.name_too_long()

	def network_create_game_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next(command_.data['game_name'])
		elif command_.data['status'] == 'invalid_game_name':
			state.invalid_game_name()
		elif command_.data['status'] == 'name_too_short':
			state.name_too_short()
		elif command_.data['status'] == 'name_too_long':
			state.name_too_long()

	def network_leave_game_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.back()

	def network_get_players_in_game_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_players(command_.data['players'])

	def network_get_games_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_games(command_.data['games'])

	def network_join_game_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next(command_.data['game_name'])
		elif command_.data['status'] == 'game_full':
			state.game_full()

	def network_logout_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.exit()

	def network_start_game_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next()
		elif command_.data['status'] == 'not_enough_players':
			state.not_enough_players()

	def network_get_player_order_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_player_order(command_.data['players'])

	def network_confirm_player_order_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next()

	def network_get_available_characters_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_available_characters(command_.data['characters'])

	def network_get_current_player_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_current_player(command_.data['player_name'])

	def network_select_character_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)

	def network_all_characters_selected_handler(self, command_, state=None):
		if command_.data['status'] == 'success':
			state.next()

	def network_get_character_selections_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_character_selections(command_.data['selections'])

	def network_confirm_character_selections_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.next()

	def network_get_player_positions_handler(self, command_, state=None):
		if command_.data['status'] == 'pending':
			command.send(command_, self.socket)
		elif command_.data['status'] == 'success':
			state.set_player_positions(command_.data['players'])
