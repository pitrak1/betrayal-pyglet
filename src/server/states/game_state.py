from src.server.states import state as state_module
from src.server import server_room_grid as server_room_grid_module
from src.shared import command as command_module
import config

class GameState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.rooms = server_room_grid_module.ServerRoomGrid()
		for player in self.players:
			self.rooms.add_player(0, 0, player)
			player.set_position(0, 0)

	def network_get_player_positions_handler(self, command, state=None):
		parsed_players = [(player.name, player.variable_name, player.grid_x, player.grid_y) for player in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })
