import socket
import threading
from src.common import command, threaded_queue, node, constants, logger
from src.server import server_player, game

class Core(node.Node):
	def __init__(self):
		super().__init__()
		self.command_queue = threaded_queue.ThreadedQueue()
		self.games = {}
		self.players = []

	def on_update(self, dt=None, state=None):
		while self.command_queue.has_elements():
			command_ = self.command_queue.pop_front()
			logger.log(f'Core handling command {command_.type} ', logger.LOG_LEVEL_COMMAND, data=command_.data)
			self.on_command(command_)

		for game_ in self.games.values():
			game_.on_update()

	def server_destroy_game_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		del self.games[command_.data['game_name']]

	def network_create_player_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		if len(command_.data['player_name']) < 6:
			command.update_and_send(command_, { 'status': 'name_too_short' })
		elif len(command_.data['player_name']) > 25:
			command.update_and_send(command_, { 'status': 'name_too_long' })
		elif any(value for value in self.players if value.name == command_.data['player_name']):
			command.update_and_send(command_, { 'status': 'invalid_player_name' })
		else:
			logger.log(f'Core creating player {command_.data["player_name"]}', logger.LOG_LEVEL_DEBUG)
			self.players.append(server_player.ServerPlayer(command_.data['player_name'], False, command_.data['connection']))
			command.update_and_send(command_, { 'status': 'success' })

	def network_create_game_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		if len(command_.data['game_name']) < 6:
			command.update_and_send(command_, { 'status': 'name_too_short' })
		elif len(command_.data['game_name']) > 40:
			command.update_and_send(command_, { 'status': 'name_too_long' })
		elif command_.data['game_name'] in self.games:
			command.update_and_send(command_, { 'status': 'invalid_game_name' })
		else:
			player = next(player for player in self.players if player == command_.data['connection'])
			player.host = True
			game_ = game.Game(command_.data['game_name'])
			self.games[command_.data['game_name']] = game_
			game_.add_player(player)
			logger.log(f'Core creating game {command_.data["game_name"]}', logger.LOG_LEVEL_DEBUG)
			command.update_and_send(command_, { 'status': 'success' })

	def network_get_games_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		command.update_and_send(command_, { 'status': 'success', 'games': [(name, len(game_.players)) for name, game_ in self.games.items()] })

	def network_join_game_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		game_ = self.games[command_.data['game_name']]
		if len(game_.players) >= constants.PLAYERS_PER_GAME:
			command.update_and_send(command_, { 'status': 'game_full' })
		else:
			player = next(player for player in self.players if player.connection == command_.data['connection'])
			player.game = game_
			game_.players.append(player)
			logger.log(f'Core adding player {player.name} to game {game_.name}', logger.LOG_LEVEL_DEBUG)
			self.add_command(command.Command('server_broadcast_players', { 'exception': player, 'connection': player.connection }))
			command.update_and_send(command_, { 'status': 'success' })

	def network_logout_handler(self, command_, state=None):
		logger.log(f'Core handling command', logger.LOG_LEVEL_COMMAND)
		player = next(p for p in self.players if p.connection == command_.data['connection'])
		if player.game: player.game.remove_player(player)
		self.players = [p for p in self.players if p.name != player.name]
		command.update_and_send(command_, { 'status': 'success' })

	def add_command(self, command_):
		logger.log(f'Adding command {command_.type} ', logger.LOG_LEVEL_COMMAND, data=command_.data)
		player = [p for p in self.players if p.connection == command_.data['connection']]
		if player and player[0].game:
			logger.log(f'Adding command {command_.type} to {player[0].game.name}', logger.LOG_LEVEL_COMMAND, data=command_.data)
			player[0].game.command_queue.append(command_)
		else:
			logger.log(f'Adding command {command_.type} to base queue', logger.LOG_LEVEL_COMMAND, data=command_.data)
			self.command_queue.append(command_)
