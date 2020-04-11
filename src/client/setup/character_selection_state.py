import pyglet
from src.client.setup import character_overview_state, character_tile
from src.client.common import label, button, state
from src.common import constants, command
import config

class CharacterSelectionState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, game_name, host, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.title = None
		self.current_player = False
		self.character_index = 0
		self.available_characters = []
		self.redraw()
		self.add_command(command.Command('network_get_available_characters', { 'status': 'pending' }))

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(3)]
			self.elements = {
				'left_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X-300, 
					y=constants.WINDOW_CENTER_Y, 
					unit_width=4, 
					unit_height=6, 
					text='Left', 
					on_click=self.go_left,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1]
				),
				'right_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X+300, 
					y=constants.WINDOW_CENTER_Y, 
					unit_width=4, 
					unit_height=6, 
					text='Right', 
					on_click=self.go_right,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1]
				)
			}

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
					group=self.groups[0]
				)

			if config.CHARACTERS[self.character_index]['variable_name'] in self.available_characters:
				if self.current_player:
					self.elements['select_button'] = button.Button(
						asset=self.asset_manager.common['button'], 
						x=constants.WINDOW_CENTER_X, 
						y=constants.WINDOW_CENTER_Y-250, 
						unit_width=12, 
						unit_height=3, 
						text='Select', 
						on_click=self.select_character,
						batch=self.batch,
						area_group=self.groups[0],
						text_group=self.groups[1]
					)
				self.elements['character_tile'] = character_tile.CharacterTile(
					asset_manager=self.asset_manager, 
					entry=config.CHARACTERS[self.character_index], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y, 
					active=True,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1],
					highlight_group=self.groups[2]
				)
			else:
				self.elements['character_tile'] = character_tile.CharacterTile(
					asset_manager=self.asset_manager, 
					entry=config.CHARACTERS[self.character_index], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y, 
					active=False,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1],
					highlight_group=self.groups[2]
				)

	def go_left(self):
		self.character_index -= 1
		if self.character_index < 0:
			self.character_index = len(config.CHARACTERS) - 1
		self.redraw()

	def go_right(self):
		self.character_index += 1
		if self.character_index > len(config.CHARACTERS) - 1:
			self.character_index = 0
		self.redraw()

	def set_available_characters(self, characters):
		self.available_characters = characters
		self.redraw()
		self.add_command(command.Command('network_get_current_player', { 'status': 'pending' }))

	def set_current_player(self, player_name):
		if player_name == 'self':
			self.title = 'You are choosing'
			self.current_player = True
		else:
			self.title = f'{player_name} is choosing'
			self.current_player = False

		self.redraw()

	def select_character(self):
		if self.current_player:
			self.add_command(command.Command(
				'network_select_character', 
				{ 'status': 'pending', 'character': config.CHARACTERS[self.character_index]['variable_name'] }
			))

	def next(self):
		self.set_state(character_overview_state.CharacterOverviewState(
			self.asset_manager, 
			self.set_state, 
			self.add_command,
			self.player_name,
			self.game_name,
			self.host,
			testing=self.testing
		))


