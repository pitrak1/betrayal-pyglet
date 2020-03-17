import pyglet
from src.shared import node as node_module
from src.client.world.common import area as area_module, button as button_module, label as label_module

class LobbyListing(node_module.Node):
	def __init__(self, asset_manager, name, players, x, y, on_click):
		super().__init__()
		self.players = players
		self.area = area_module.Area(asset_manager.common['brown_button'], x, y, 26, 2, 'left')
		self.lobby_name = label_module.Label(name, x=x, y=y, anchor_x='left', anchor_y='center', align='left', font_size=15)
		self.player_count = label_module.Label(f'{players}/6', x=x + 390, y=y, anchor_x='right', anchor_y='center', align='right', font_size=15)
		self.on_click = on_click

	def draw(self):
		self.area.draw()
		self.lobby_name.draw()
		self.player_count.draw()

	def client_translated_mouse_press_handler(self, command, state=None):
		if self.area.within_bounds(command.data['x'], command.data['y']):
			self.on_click()	
