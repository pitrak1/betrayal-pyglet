from lattice2d.components import Area, Label, Component
from constants import PLAYERS_PER_GAME

class GameListing(Component):
	def __init__(self, name, players, position, on_click):
		super().__init__()
		self.__area = Area(
			position=position,
			unit_dimensions=(13, 2),
			align='left'
		)
		self.__game_name = Label(
			text=name,
			x=position[0],
			y=position[1],
			anchor_x='left',
			anchor_y='center',
			align='left',
			font_size=15,
			color=(0, 0, 0, 255)
		)
		self.__player_count = Label(
			text=f'{players}/{PLAYERS_PER_GAME}',
			x=position[0] + 390,
			y=position[1],
			anchor_x='right',
			anchor_y='center',
			align='right',
			font_size=15,
			color=(0, 0, 0, 255)
		)
		self.__on_click = on_click

	def register(self, layer):
		self.__area.register(layer)
		self.__game_name.register(layer)
		self.__player_count.register(layer)

	def mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds((command.data['x'], command.data['y'])):
			self.__on_click()