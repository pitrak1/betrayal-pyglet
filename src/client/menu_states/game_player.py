import pyglet
from lattice2d.components import Area, Label, Component
from lattice2d.client import Assets

class GamePlayer(Component):
	def __init__(self, name, host, position):
		super().__init__()
		self.__area = Area(
			position=position, 
			unit_dimensions=(13, 2), 
			align='left'
		)
		self.__player_name = Label(
			text=name,
			x=position[0], 
			y=position[1], 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15,
			color=(0, 0, 0, 255)
		)
		self.__crown = None
		if host:
			self.__crown = pyglet.sprite.Sprite(
				Assets().custom['host_marker'], 
				x=position[0] + 390, 
				y=position[1]
			)

	def register(self, layer):
		self.__area.register(layer)
		self.__player_name.batch = layer.batch
		self.__player_name.group = layer.groups[1]
		if self.__crown:
			self.__crown.batch = layer.batch
			self.__crown.group = layer.groups[1]