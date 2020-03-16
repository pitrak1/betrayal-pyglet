from src.client.states import state as state_module
from src.client.world.game import client_room_grid as client_room_grid_module, client_player as client_player_module, client_character as client_character_module
from src.client.world.common import button as button_module, label as label_module
from src.shared import constants, command as command_module
import config

class GameState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.rooms = client_room_grid_module.ClientRoomGrid(self.asset_manager)
		self.elements = [self.rooms]
		self.players = []
		self.characters = {}
		for character in config.STARTING_CHARACTERS:
			self.characters[character['variable_name']] = client_character_module.ClientCharacter(character, self.asset_manager)
		self.add_command(command_module.Command('network_get_player_positions', { 'status': 'pending' }))

	def set_player_positions(self, players):
		for player_tuple in players:
			name, character, grid_x, grid_y = player_tuple
			player = client_player_module.ClientPlayer(self.characters[character].entry, self.asset_manager, name, int(grid_x), int(grid_y))
			self.players.append(player)
			self.rooms.add_player(int(grid_x), int(grid_y), player)


	def select(self, node):
		self.add_command(command_module.Command('client_select', { 'selected': node }))

	def draw(self):
		for element in self.elements:
			element.draw()
