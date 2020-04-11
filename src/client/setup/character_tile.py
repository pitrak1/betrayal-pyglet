import pyglet
from src.common import node
from src.client.common import label, area

class CharacterTile(node.Node):
	def __init__(self, asset_manager, entry, x, y, active, batch, area_group, text_group, highlight_group):
		super().__init__()
		self.__area = area.Area(
			asset=asset_manager.common['area'], 
			x=x, 
			y=y + 60, 
			unit_width=16, 
			unit_height=24,
			batch=batch,
			group=area_group
		)
		self.__name_label = label.Label(
			text=entry['display_name'], 
			x=x, 
			y=y + 230, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=15,
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__picture = pyglet.sprite.Sprite(
			asset_manager.characters[entry['variable_name']], 
			x=x, 
			y=y + 120, 
			batch=batch,
			group=text_group
		)

		speed_text = 'SPD: '
		for value in entry['speed']:
			speed_text += f'{value} '
		self.__speed_label = label.Label(
			text=speed_text, 
			x=x, 
			y=y + 15, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__speed_indicator = pyglet.sprite.Sprite(
			asset_manager.common['attribute_highlight'], 
			x=x - 60 + 20 * entry['speed_index'], 
			y=y + 15, 
			batch=batch,
			group=highlight_group
		)

		might_text = 'MGT: '
		for value in entry['might']:
			might_text += f'{value} '
		self.__might_label = label.Label(
			text=might_text, 
			x=x, 
			y=y - 25, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255),
			batch=batch,
			group=text_group
		)
		self.__might_indicator = pyglet.sprite.Sprite(
			asset_manager.common['attribute_highlight'], 
			x=x - 60 + 20 * entry['might_index'], 
			y=y - 25,
			batch=batch,
			group=highlight_group
		)

		sanity_text = 'SAN: '
		for value in entry['sanity']:
			sanity_text += f'{value} '
		self.__sanity_label = label.Label(
			text=sanity_text, 
			x=x, 
			y=y - 65, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__sanity_indicator = pyglet.sprite.Sprite(
			asset_manager.common['attribute_highlight'], 
			x=x - 60 + 20 * entry['sanity_index'], 
			y=y - 65,
			batch=batch,
			group=highlight_group
		)

		knowledge_text = 'KNW: '
		for value in entry['knowledge']:
			knowledge_text += f'{value} '
		self.__knowledge_label = label.Label(
			text=knowledge_text, 
			x=x, 
			y=y - 105, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__knowledge_indicator = pyglet.sprite.Sprite(
			asset_manager.common['attribute_highlight'], 
			x=x - 60 + 20 * entry['knowledge_index'], 
			y=y - 105,
			batch=batch,
			group=highlight_group
		)

		if not active:
			self.__active_label = label.Label(
				text='NOT ACTIVE', 
				x=x, 
				y=y + 215, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=12, 
				color=(0, 0, 0, 255), 
				batch=batch,
				group=text_group
			)

