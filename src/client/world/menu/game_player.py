import pyglet
from src.shared import node
from src.client.world.common import area, label

class GamePlayer(node.Node):
	def __init__(self, asset_manager, name, host, x, y, batch, area_group, text_group):
		super().__init__()
		self.__area = area.Area(
			asset=asset_manager.common['button'], 
			x=x, 
			y=y, 
			unit_width=26, 
			unit_height=2, 
			align='left',
			batch=batch,
			group=area_group
		)
		self.__player_name = label.Label(
			text=name, 
			x=x, 
			y=y, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		if host:
			self.__crown = pyglet.sprite.Sprite(
				asset_manager.common['host_marker'], 
				x=x + 390, 
				y=y,
				batch=batch,
				group=text_group
			)
