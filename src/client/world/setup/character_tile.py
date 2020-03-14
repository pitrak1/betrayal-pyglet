import pyglet
from src.shared import node as node_module
from src.client.world.common import label as label_module
from src.client.world.common import area as area_module

class CharacterTile(node_module.Node):
	def __init__(self, asset_manager, entry, x, y, on_click):
		super().__init__()
		self.entry = entry
		self.area = area_module.Area(asset_manager.common['white_button'], x, y, 8, 16)
		self.on_click = on_click
		self.batch = pyglet.graphics.Batch()
		self.name_label = label_module.Label(entry['display_name'], x=x, y=y + 115, anchor_x='center', anchor_y='center', align='center', font_size=10, color=(0, 0, 0, 255), batch=self.batch)

		self.picture = pyglet.sprite.Sprite(asset_manager.characters[entry['variable_name']], x, y + 45, batch=self.batch)
		self.picture.update(scale_x=0.7, scale_y=0.7)

		speed_text = 'SPD: '
		for value in entry['speed']:
			speed_text += f'{value} '
		self.speed_label = label_module.Label(speed_text, x=x, y=y - 35, anchor_x='center', anchor_y='center', align='center', font_size=8, color=(0, 0, 0, 255), batch=self.batch)
		self.speed_indicator = pyglet.sprite.Sprite(asset_manager.misc['attribute_highlight'], x - 23 + 9 * entry['speed_index'], y - 35, batch=self.batch)

		might_text = 'MGT: '
		for value in entry['might']:
			might_text += f'{value} '
		self.might_label = label_module.Label(might_text, x=x, y=y - 55, anchor_x='center', anchor_y='center', align='center', font_size=8, color=(0, 0, 0, 255), batch=self.batch)
		self.might_indicator = pyglet.sprite.Sprite(asset_manager.misc['attribute_highlight'], x - 23 + 9 * entry['might_index'], y - 55, batch=self.batch)

		sanity_text = 'SAN: '
		for value in entry['sanity']:
			sanity_text += f'{value} '
		self.sanity_label = label_module.Label(sanity_text, x=x, y=y - 75, anchor_x='center', anchor_y='center', align='center', font_size=8, color=(0, 0, 0, 255), batch=self.batch)
		self.sanity_indicator = pyglet.sprite.Sprite(asset_manager.misc['attribute_highlight'], x - 23 + 9 * entry['sanity_index'], y - 75, batch=self.batch)

		knowledge_text = 'KNW: '
		for value in entry['knowledge']:
			knowledge_text += f'{value} '
		self.knowledge_label = label_module.Label(knowledge_text, x=x, y=y - 95, anchor_x='center', anchor_y='center', align='center', font_size=8, color=(0, 0, 0, 255), batch=self.batch)
		self.knowledge_indicator = pyglet.sprite.Sprite(asset_manager.misc['attribute_highlight'], x - 23 + 9 * entry['knowledge_index'], y - 95, batch=self.batch)

	def draw(self):
		self.area.draw()
		self.batch.draw()

	def client_translated_mouse_press_handler(self, command, state):
		if self.on_click and self.area.within_bounds(command.data['x'], command.data['y']):
			self.on_click(self.entry['variable_name'])	
