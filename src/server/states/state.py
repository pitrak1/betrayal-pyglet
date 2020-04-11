from src.common import command, logger, node

class State(node.Node):
	def __init__(self, game):
		super().__init__()
		self.game = game

	def network_get_players_in_game_handler(self, command_, state=None):
		logger.log(f'State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.game.send_players_in_game(command_.data['exception'])

	def server_broadcast_players_handler(self, command_, state=None):
		logger.log(f'State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.game.send_players_in_game(command_.data['exception'])

	def network_leave_game_handler(self, command_, state=None):
		logger.log(f'State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		player = next(p for p in self.game.players if command_.data['connection'] == p)
		self.game.remove_player(player)
