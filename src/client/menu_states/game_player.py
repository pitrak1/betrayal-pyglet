import pyglet
from lattice2d.client.components.area import Area
from lattice2d.client.components.label import Label
from lattice2d.nodes.node import Node
from lattice2d.client.assets import Assets

class GamePlayer(Node):
	def __init__(self, name, host, position, batch, area_group, text_group):
		super().__init__()
		self.__area = Area(
			position=position, 
			unit_dimensions=(13, 2), 
			align='left',
			batch=batch,
			group=area_group
		)
		self.__player_name = Label(
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
		if host:
			self.__crown = pyglet.sprite.Sprite(
				Assets().custom['host_marker'], 
				x=position[0] + 390, 
				y=position[1],
				batch=batch,
				group=text_group
			)