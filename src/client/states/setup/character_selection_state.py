import pyglet
from src.client.states.setup import character_overview_state
from src.client.world.common import label, button
from src.client.world.setup import character_tile
from src.client.states import state
from src.shared import constants, command
import config

class CharacterSelectionState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.__title = None
		self.__current_player = False
		self.__character_index = 0
		self.__available_characters = []
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_available_characters', { 'status': 'pending' }))

	def __create_base_elements(self):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(3)]
		elements = [
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X-300, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=4, 
				unit_height=6, 
				text='Left', 
				on_click=self.__go_left,
				batch=self._batch,
				area_group=self.__groups[0],
				text_group=self.__groups[1]
			),
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X+300, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=4, 
				unit_height=6, 
				text='Right', 
				on_click=self.__go_right,
				batch=self._batch,
				area_group=self.__groups[0],
				text_group=self.__groups[1]
			)
		]

		if self.__title:
			elements.append(label.Label(
				text=self.__title, 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_HEIGHT - 40, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			))

		if config.CHARACTERS[self.__character_index]['variable_name'] in self.__available_characters:
			if self.__current_player:
				elements.append(button.Button(
					asset=self._data['assets'].common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y-250, 
					unit_width=12, 
					unit_height=3, 
					text='Select', 
					on_click=self.__select_character,
					batch=self._batch,
					area_group=self.__groups[0],
					text_group=self.__groups[1]
				))
			elements.append(character_tile.CharacterTile(
				asset_manager=self._data['assets'], 
				entry=config.CHARACTERS[self.__character_index], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				active=True,
				batch=self._batch,
				area_group=self.__groups[0],
				text_group=self.__groups[1],
				highlight_group=self.__groups[2]
			))
		else:
			elements.append(character_tile.CharacterTile(
				asset_manager=self._data['assets'], 
				entry=config.CHARACTERS[self.__character_index], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				active=False,
				batch=self._batch,
				area_group=self.__groups[0],
				text_group=self.__groups[1],
				highlight_group=self.__groups[2]
			))

		return elements

	def __go_left(self):
		self.__character_index -= 1
		if self.__character_index < 0:
			self.__character_index = len(config.CHARACTERS) - 1
		self._elements = self.__create_base_elements()

	def __go_right(self):
		self.__character_index += 1
		if self.__character_index > len(config.CHARACTERS) - 1:
			self.__character_index = 0
		self._elements = self.__create_base_elements()

	def set_available_characters(self, characters):
		self.__available_characters = characters
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_current_player', { 'status': 'pending' }))

	def set_current_player(self, player_name):
		if player_name == 'self':
			self.__title = 'You are choosing'
			self.__current_player = True
		else:
			self.__title = f'{player_name} is choosing'
			self.__current_player = False

		self._elements = self.__create_base_elements()

	def __select_character(self):
		if self.__current_player:
			self._add_command(command.Command('network_select_character', { 'status': 'pending', 'character': config.CHARACTERS[self.__character_index]['variable_name'] }))

	def all_characters_selected(self):
		self._set_state(character_overview_state.CharacterOverviewState(
			self._data, 
			self._set_state, 
			self._add_command
		))


