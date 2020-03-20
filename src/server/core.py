import socket
import threading
from src.shared import command as command_module, threaded_queue, node, constants
from src.server import player as player_module, game as game_module

class Core(node.Node):
	def __init__(self):
		super().__init__()
		self.command_queue = threaded_queue.ThreadedQueue()
		self.games = {}
		self.players = []

	def on_update(self, dt=None, state=None):
		while self.command_queue.has_elements():
			command = self.command_queue.pop_front()
			print(f'popped {command.type}')
			self.on_command(command)

		for game in self.games.values():
			game.on_update()

	def server_destroy_game_handler(self, command, state=None):
		del self.games[command.data['game_name']]

	def network_create_player_handler(self, command, state=None):
		if len(command.data['player_name']) < 6:
			command_module.update_and_send(command, { 'status': 'name_too_short' })
		elif len(command.data['player_name']) > 25:
			command_module.update_and_send(command, { 'status': 'name_too_long' })
		elif any(value for value in self.players if value.name == command.data['player_name']):
			command_module.update_and_send(command, { 'status': 'invalid_player_name' })
		else:
			self.players.append(player_module.Player(command.data['player_name'], False, command.data['connection']))
			command_module.update_and_send(command, { 'status': 'success' })

	def network_create_game_handler(self, command, state=None):
		if len(command.data['game_name']) < 6:
			command_module.update_and_send(command, { 'status': 'name_too_short' })
		elif len(command.data['game_name']) > 40:
			command_module.update_and_send(command, { 'status': 'name_too_long' })
		elif command.data['game_name'] in self.games:
			command_module.update_and_send(command, { 'status': 'invalid_game_name' })
		else:
			player = next(player for player in self.players if player == command.data['connection'])
			player.host = True
			game = game_module.Game(command.data['game_name'])
			self.games[command.data['game_name']] = game
			player.game = game
			game.players.append(player)
			command_module.update_and_send(command, { 'status': 'success' })

	def network_get_games_handler(self, command, state=None):
		command_module.update_and_send(command, { 'status': 'success', 'games': [(name, len(game.players)) for name, game in self.games.items()] })

	def network_join_game_handler(self, command, state=None):
		game = self.games[command.data['game_name']]
		if len(game.players) > constants.PLAYERS_PER_GAME:
			command_module.update_and_send(command, { 'status': 'game_full' })
		else:
			player = next(player for player in self.players if player == command.data['connection'])
			game = self.games[command.data['game_name']]
			player.game = game
			game.players.append(player)
			self.add_command(command_module.Command('server_broadcast_players', { 'exception': player, 'connection': player.connection }))
			command_module.update_and_send(command, { 'status': 'success' })

	def network_logout_handler(self, command, state=None):
		player = next(p for p in self.players if p == command.data['connection'])
		if player.game: self.__leave_game(player)
		self.players = [p for p in self.players if p.name != player.name]
		command_module.update_and_send(command, { 'status': 'success' })

	def __leave_game(self, player):
		player.game.players.remove(player)
		if player.game.players:
			self.add_command(command_module.Command('server_broadcast_players', { 'exception': None, 'connection': player.connection }))
		else:
			del self.games[player.game.name]
		player.game = None

	def add_command(self, command): 
		player = [p for p in self.players if p == command.data['connection']]
		if player and player[0].game:
			player[0].game.command_queue.append(command)
		else:
			self.command_queue.append(command)
