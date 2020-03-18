import pyglet
from src.shared import node as node_module
from src.client.world.common import area as area_module, label as label_module

class GamePlayer(node_module.Node):
	def __init__(self, asset_manager, name, host, x, y):
		super().__init__()
		self.host = host
		self.area = area_module.Area(asset_manager.common['button'], x, y, 26, 2, 'left')
		self.player_name = label_module.Label(name, x=x, y=y, anchor_x='left', anchor_y='center', align='left', font_size=15)
		self.crown = pyglet.sprite.Sprite(asset_manager.common['host_marker'], x=x + 390, y=y)

	def draw(self):
		self.area.draw()
		self.player_name.draw()
		if self.host: self.crown.draw()

