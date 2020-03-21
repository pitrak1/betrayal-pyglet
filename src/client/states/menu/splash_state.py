import pyglet
from src.client.world.common import background, button, area, label
from src.client.states import state
from src.client.states.menu import create_player_state
from src.shared import constants

class SplashState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
		self._elements = [
			background.Background(
				asset=self._data['assets'].common['menu_background'],
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
				text='Begin', 
				on_click=self.__begin,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			)
		]

	def __begin(self):
		self._set_state(create_player_state.CreatePlayerState(
			self._data,
			self._set_state, 
			self._add_command
		))
