import sys
import pyglet
from src.client.world.common import button, text_box, area, background, label
from src.client.states import state
from src.client.states.menu import main_menu_state, game_state
from src.shared import constants, command

class CreateGameState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
		self.__game_name_text_box = text_box.TextBox(
			asset=data['assets'].common['text_box'], 
			x=constants.WINDOW_CENTER_X - 200, 
			y=constants.WINDOW_CENTER_Y + 50, 
			unit_width=26, 
			label_text='Game Name',
			max_length=40,
			batch=self._batch,
			area_group=self.__groups[2],
			text_group=self.__groups[3]
		)
		self._elements = [
			background.Background(
				asset=data['assets'].common['menu_background'],
				batch=self._batch,
				group=self.__groups[0]
			),
			area.Area(
				asset=data['assets'].common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=40, 
				unit_height=30, 
				opacity=192,
				batch=self._batch,
				group=self.__groups[1]
			),
			label.Label(
				text='Create Game', 
				x=constants.WINDOW_CENTER_X,
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(0, 0, 0, 255),
				batch=self._batch,
				group=self.__groups[2]
			),
			self.__game_name_text_box,
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X - 150, 
				y=constants.WINDOW_CENTER_Y - 100, 
				unit_width=12, 
				unit_height=3, 
				text='Back', 
				on_click=self.__back,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 100, 
				unit_width=12, 
				unit_height=3, 
				text='Create', 
				on_click=self.__create,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			)
		]

	def __back(self):
		self._set_state(main_menu_state.MainMenuState(
			self._data,
			self._set_state, 
			self._add_command
		))

	def invalid_game_name(self):
		self.__game_name_text_box.set_error_text('name is already in use')

	def name_too_short(self):
		self.__game_name_text_box.set_error_text('must be 6 characters or more')

	def name_too_long(self):
		self.__game_name_text_box.set_error_text('must be 40 characters or less')

	def __create(self):
		game_name = self.__game_name_text_box.get_text()
		if len(game_name) < 6:
			self.__game_name_text_box.set_error_text('must be 6 characters or more')
		else:
			self._add_command(command.Command('network_create_game', { 'status': 'pending', 'game_name': game_name }))

	def next(self, game_name):
		self._data.update({ 'game_name': game_name, 'host': True })
		self._set_state(game_state.GameState(
			self._data,
			self._set_state, 
			self._add_command
		))
