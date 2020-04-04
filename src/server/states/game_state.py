from src.server.states import state as state_module
from src.server import server_room_grid as server_room_grid_module
from src.shared import command as command_module, logger
import config

class GameState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.name = data['name']
		self.current_player_index = 0
		self.rooms = server_room_grid_module.ServerRoomGrid()
		for player in self.players:
			self.rooms.add_player(0, 0, player)
			player.set_position(0, 0)

	def network_get_player_positions_handler(self, command, state=None):
		logger.log(f'Game State {self.name} done waiting', logger.LOG_LEVEL_DEBUG)
		parsed_players = [(player.name, player.variable_name, player.grid_x, player.grid_y) for player in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })

	def network_get_current_player_handler(self, command, state=None):
		logger.log(f'Game State {self.name} done waiting', logger.LOG_LEVEL_DEBUG)
		if command.data['connection'] == self.players[self.current_player_index]:
			player_name = 'self'
		else:
			player_name = self.players[self.current_player_index].name
		command_module.update_and_send(command, { 'status': 'success', 'player_name': player_name })
