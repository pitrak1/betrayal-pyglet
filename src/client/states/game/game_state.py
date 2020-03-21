import pyglet
from src.client.states import state
from src.client.world.game import client_room_grid, client_player
from src.client.world.common import button, label
from src.shared import constants, command
import config

class GameState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.__rooms = client_room_grid.ClientRoomGrid()
		self._elements = [self.__rooms]
		self._add_command(command.Command('client_redraw'))
		# self.__players = []
		# self._add_command(command.Command('network_get_player_positions', { 'status': 'pending' }))

	def client_redraw_handler(self, command, state=None):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(constants.NUMBER_OF_GROUPS)]
		command.data.update({ 'asset_manager': self._data['assets'], 'batch': self._batch, 'groups': self.__groups })
		self.__rooms.on_command(command, state)

	# def set_player_positions(self, players):
	# 	for player_tuple in players:
	# 		print(player_tuple)
	# 		# name, character, grid_x, grid_y = player_tuple
	# 		# player = client_player.ClientPlayer(config.CHARACTERS[character], self._data['assets'], name, int(grid_x), int(grid_y))
	# 		# self.players.append(player)
	# 		# self.rooms.add_player(int(grid_x), int(grid_y), player)


	# def select(self, node):
	# 	self._add_command(command.Command('client_select', { 'selected': node }))
	# 	self._add_command(command.Command('client_redraw'))
