import sys
import pyglet
from src.client.world.common import background, button, text_box, area, label
from src.client.states import state
from src.client.states.menu import main_menu_state
from src.shared import constants, command

class CreatePlayerState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.__layers = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
		self.__player_name_text_box = text_box.TextBox(
			asset=data['assets'].common['text_box'], 
			x=constants.WINDOW_CENTER_X - 120, 
			y=constants.WINDOW_CENTER_Y + 50, 
			unit_width=16,
			label_text='Player Name',
			max_length=25,
			batch=self._batch,
			area_group=self.__layers[2],
			text_group=self.__layers[3]
		)
		self._elements = [
			background.Background(
				asset=data['assets'].common['menu_background'],
				batch=self._batch,
				group=self.__layers[0]
			),
			area.Area(
				asset=data['assets'].common['area'],
				x=constants.WINDOW_CENTER_X,
				y=constants.WINDOW_CENTER_Y,
				unit_width=20,
				unit_height=30,
				batch=self._batch,
				group=self.__layers[1],
				opacity=192
			),
			label.Label(
				text='Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self._batch,
				group=self.__layers[2]
			),
			self.__player_name_text_box,
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 50, 
				unit_width=12, 
				unit_height=3, 
				text='Continue', 
				on_click=self.__submit,
				batch=self._batch,
				area_group=self.__layers[2],
				text_group=self.__layers[3]
			),
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 110, 
				unit_width=12, 
				unit_height=3, 
				text='Exit', 
				on_click=self.__exit,
				batch=self._batch,
				area_group=self.__layers[2],
				text_group=self.__layers[3]
			)
		]

	def __exit(self):
		sys.exit()

	def __submit(self):
		player_name = self.__player_name_text_box.get_text()
		if len(player_name) < 6:
			self.__player_name_text_box.set_error_text('must be 6 characters or more')
		else:
			self._add_command(command.Command('network_create_player', { 'status': 'pending', 'player_name': player_name }))

	def invalid_player_name(self):
		self.__player_name_text_box.set_error_text('name is already in use')

	def name_too_short(self):
		self.__player_name_text_box.set_error_text('must be 6 characters or more')

	def name_too_long(self):
		self.__player_name_text_box.set_error_text('must be 25 characters or less')

	def next(self, player_name):
		self._data.update({ 'player_name': player_name })
		self._set_state(main_menu_state.MainMenuState(
			self._data,
			self._set_state, 
			self._add_command
		))
