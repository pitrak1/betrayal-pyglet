import pyglet
from src.client.states import state
from src.client.world.game import client_room_grid, client_player
from src.client.world.common import button, label
from src.shared import constants, command
import config

class GameState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(constants.NUMBER_OF_GROUPS)]
		self.__rooms = client_room_grid.ClientRoomGrid()
		self._elements = [self.__rooms]
		self.__players = []
		self.__current_player = False
		self._add_command(command.Command('network_get_player_positions', { 'status': 'pending' }))
		
	def client_redraw_handler(self, command, state=None):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(constants.NUMBER_OF_GROUPS)]
		command.data.update({ 'asset_manager': self._data['assets'], 'batch': self._batch, 'groups': self.__groups })
		self.__rooms.on_command(command, state)
		if self.__title:
			self.__title_label = label.Label(
				text=self.__title, 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_HEIGHT - 40, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[constants.HIGHLIGHTS_GROUP]
			)

	def set_player_positions(self, players):
		for player_tuple in players:
			name, character, grid_x, grid_y = player_tuple
			player = client_player.ClientPlayer(
				next(c for c in config.CHARACTERS if c['variable_name'] == character), 
				name,
				self._data['host'],
				self._data['player_name'] == name
			)
			self.__players.append(player)
			self.__rooms.add_player(int(grid_x), int(grid_y), player)
			self._add_command(command.Command('network_get_current_player', { 'status': 'pending' }))

	def set_current_player(self, player_name):
		if player_name == 'self':
			self.__title = 'Your turn'
			self.__current_player = True
		else:
			self.__title = f'{player_name}\'s turn'
			self.__current_player = False

		self._add_command(command.Command('client_redraw'))

	def select(self, node):
		self._add_command(command.Command('client_select', { 'selected': node }))
		self._add_command(command.Command('client_redraw'))
