import random
import threading
from src.server.states import lobby_state
from src.common import threaded_queue, stringify, threaded_sync, node, logger, command
import config

class Game(node.Node):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.players = []
		self.rooms = []
		self.command_queue = threaded_queue.ThreadedQueue()
		self.current_state = lobby_state.LobbyState(self)

	def set_state(self, state):
		self.current_state = state

	def add_command(self, command):
		self.command_queue.append(command)

	def on_update(self, dt=None, state=None):
		while self.command_queue.has_elements():
			command = self.command_queue.pop_front()
			logger.log(f'Game {self.name} handling command {command.type} ', logger.LOG_LEVEL_COMMAND, data=command.data)
			self.current_state.on_command(command)

	def add_player(self, player):
		player.game = self
		self.players.append(player)

	def remove_player(self, player):
		player.game = None
		self.players.remove(player)
		if self.players:
			logger.log(f'Game {self.name} broadcasting players', logger.LOG_LEVEL_DEBUG)
			self.send_players_in_game()
		else:
			self.add_command(command.Command('server_destroy_game', { 'game_name': self.name }))

	def send_players_in_game(self, exception=None):
		parsed_players = [(p.name, p.host) for p in self.players]
		players = [p for p in self.players if p != exception]
		command.create_and_send_to_all('network_get_players_in_game', { 'status': 'success', 'players': parsed_players }, players)
