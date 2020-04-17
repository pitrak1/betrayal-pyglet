import pyglet
from src.client.game import client_room_grid, client_player
from src.client.common import button, label, state
from src.common import constants, command, logger
import config

class ClientGameState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, game_name, host, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.rooms = client_room_grid.ClientRoomGrid(testing)
		self.players = []
		self.current_player = False
		self.title = None
		self.redraw()
		self.add_command(command.Command('network_get_player_positions', { 'status': 'pending' }))

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(constants.NUMBER_OF_GROUPS)]
			self.elements = { 'rooms': self.rooms }
			if self.title:
				self.elements['title'] = label.Label(
					text=self.title, 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_HEIGHT - 40, 
					anchor_x='center', 
					anchor_y='center', 
					align='center', 
					font_size=25, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[constants.HIGHLIGHTS_GROUP]
				)
		
	def client_redraw_handler(self, command, state=None):
		logger.log('Game State handling command', logger.LOG_LEVEL_COMMAND)
		self.redraw()
		command.data.update({ 'asset_manager': self.asset_manager, 'batch': self.batch, 'groups': self.groups })
		self.rooms.on_command(command, state)

	def set_player_positions(self, players):
		for player_tuple in players:
			name, character, grid_x, grid_y = player_tuple
			entry = next(c for c in config.CHARACTERS if c['variable_name'] == character)
			self_ = name == self.player_name
			player = client_player.ClientPlayer(entry, name, self.host, self_, self.testing)
			self.players.append(player)
			self.rooms.add_player(int(grid_x), int(grid_y), player)
		self.add_command(command.Command('network_get_current_player', { 'status': 'pending' }))

	def set_current_player(self, player_name):
		if player_name == 'self':
			self.title = 'Your turn'
			self.current_player = True
		else:
			self.title = f'{player_name}\'s turn'
			self.current_player = False

		self.add_command(command.Command('client_redraw'))

	def select(self, node):
		self.selected = node
		self.add_command(command.Command('client_select', { 'selected': node }))
		self.add_command(command.Command('client_redraw'))

	# def trigger_selected_character_move(self, grid_x, grid_y):
	# 	if self.current_player and self.selected and isinstance(self.selected, client_player.ClientPlayer):
	# 		if self.selected.self_ and self.rooms.can_move(self.selected.grid_x, self.selected.grid_y, grid_x, grid_y):
	# 			self.rooms.move(self.selected, self.selected.grid_x, self.selected.grid_y, grid_x, grid_y)
	# 			self.add_command(command.Command('client_redraw'))

