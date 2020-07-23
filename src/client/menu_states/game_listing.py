from lattice2d.client.components.area import Area
from lattice2d.client.components.label import Label
from lattice2d.nodes.node import Node
from constants import PLAYERS_PER_GAME

class GameListing(Node):
	def __init__(self, name, players, position, on_click, batch, area_group, text_group):
		super().__init__()
		self.name = name
		self.__area = Area(
			position=position,
			unit_dimensions=(13, 2),
			align='left',
			batch=batch,
			group=area_group
		)
		self.__game_name = Label(
			text=name, 
			x=position[0], 
			y=position[1], 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		self.__player_count = Label(
			text=f'{players}/{PLAYERS_PER_GAME}', 
			x=position[0] + 390, 
			y=position[1], 
			anchor_x='right', 
			anchor_y='center', 
			align='right', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		self.__on_click = on_click

	def mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds((command.data['x'], command.data['y'])):
			self.__on_click()