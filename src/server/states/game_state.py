from src.server import server_room_grid as server_room_grid_module
from src.shared import command as command_module, logger
import config

class GameState():
	def __init__(self, game):
		super().__init__(game)
		self.current_player_index = 0
		self.game.rooms = server_room_grid_module.ServerRoomGrid()
		for player in self.game.players:
			self.game.rooms.add_player(0, 0, player)
			player.set_position(0, 0)

	def network_get_player_positions_handler(self, command, state=None):
		logger.log(f'Game State {self.game.name} done waiting', logger.LOG_LEVEL_DEBUG)
		parsed_players = [(player.name, player.variable_name, player.grid_x, player.grid_y) for player in self.game.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })

	def network_get_current_player_handler(self, command, state=None):
		logger.log(f'Game State {self.game.name} done waiting', logger.LOG_LEVEL_DEBUG)
		if command.data['connection'] == self.game.players[self.current_player_index]:
			player_name = 'self'
		else:
			player_name = self.game.players[self.current_player_index].name
		command_module.update_and_send(command, { 'status': 'success', 'player_name': player_name })
