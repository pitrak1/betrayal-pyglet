import pyglet
from src.client.states import state
from src.client.states.game import game_state
from src.client.world.common import button, label 
from src.shared import constants, command

class CharacterOverviewState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_character_selections', { 'status': 'pending' }))
		self._waiting = False

	def __create_base_elements(self):
		self._batch = pyglet.graphics.Batch()
		self.__layers = [pyglet.graphics.OrderedGroup(i) for i in range(2)]

		return [
			label.Label(
				text='The players\' selected characters are:', 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_HEIGHT - 40, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__layers[0]
			),
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 200, 
				unit_width=12, 
				unit_height=3, 
				text='Begin', 
				on_click=self.__confirm_characters,
				batch=self._batch,
				area_group=self.__layers[0],
				text_group=self.__layers[1]
			)
		]

	def set_character_selections(self, selections):
		self._elements = self.__create_base_elements()
		count = 0
		for selection in selections:
			label_text = f'{selection[0]}: {selection[1]}'
			self._elements.append(label.Label(
				text=label_text, 
				x=constants.WINDOW_CENTER_X - 180, 
				y=constants.WINDOW_CENTER_Y + 130 - (40 * count), 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=18, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__layers[0]
			))
			count += 1

	def __confirm_characters(self):
		if not self._waiting:
			self._waiting = True
			self._elements.append(label.Label(
				text='Waiting for other players...', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 260, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__layers[0]
			))
			self._add_command(command.Command('network_confirm_character_selections', { 'status': 'pending' }))

	def next(self):
		self._set_state(game_state.GameState(self._data, self._set_state, self._add_command))
