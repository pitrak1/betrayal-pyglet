import pyglet
from src.shared import node, constants
from src.client.world.common import area, button, label

class GameListing(node.Node):
	def __init__(self, asset_manager, name, players, x, y, on_click, batch, area_group, text_group):
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
		self.__game_name = label.Label(
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
		self.__player_count = label.Label(
			text=f'{players}/{constants.PLAYERS_PER_GAME}', 
			x=x + 390, 
			y=y, 
			anchor_x='right', 
			anchor_y='center', 
			align='right', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		self.__on_click = on_click

	def client_translated_mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds(command.data['x'], command.data['y']):
			self.__on_click()	
