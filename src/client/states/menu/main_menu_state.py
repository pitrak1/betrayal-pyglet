import sys
import pyglet
from src.client.world.common import background, button, area, label
from src.client.states import state
from src.client.states.menu import create_game_state, game_list_state
from src.shared import constants, command

class MainMenuState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
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
				unit_width=20, 
				unit_height=30,
				batch=self._batch,
				group=self.__groups[1],
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
				group=self.__groups[2]
			),
			button.Button(
				asset=data['assets'].common['button'],
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 50, 
				unit_width=12, 
				unit_height=3, 
				text='Create Game', 
				on_click=self.__create_game,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 30, 
				unit_width=12, 
				unit_height=3,
				text='Join Game', 
				on_click=self.__join_game,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			button.Button(
				asset=data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 110, 
				unit_width=12, 
				unit_height=3, 
				text='Exit', 
				on_click=self.__start_exit,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			)
		]

	def __start_exit(self):
		self._add_command(command.Command('network_logout', { 'status': 'pending' }))

	def exit(self):
		sys.exit()

	def __create_game(self):
		self._set_state(create_game_state.CreateGameState(
			self._data,
			self._set_state, 
			self._add_command
		))

	def __join_game(self):
		self._set_state(game_list_state.GameListState(
			self._data,
			self._set_state, 
			self._add_command
		))

	

