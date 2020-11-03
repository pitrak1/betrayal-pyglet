import pyglet
from lattice2d.components import Area, Label
from lattice2d.nodes import Node
from lattice2d.client import Assets
from constants import WINDOW_CENTER

class CharacterTile(Node):
	def __init__(self, entry, position, active, batch, area_group, text_group, highlight_group):
		super().__init__()
		self.__area = Area(
			position=(position[0], position[1] + 60), 
			unit_dimensions=(8, 12),
			batch=batch,
			group=area_group
		)
		self.__name_label = Label(
			text=entry['display_name'], 
			x=position[0], 
			y=position[1] + 230, 
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
			Assets().characters[entry['variable_name']], 
			x=position[0], 
			y=position[1] + 120, 
			batch=batch,
			group=text_group
		)

		speed_text = 'SPD: '
		for value in entry['speed']:
			speed_text += f'{value} '
		self.__speed_label = Label(
			text=speed_text, 
			x=position[0], 
			y=position[1] + 15, 
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
			Assets().custom['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['speed_index'], 
			y=position[1] + 15, 
			batch=batch,
			group=highlight_group
		)

		might_text = 'MGT: '
		for value in entry['might']:
			might_text += f'{value} '
		self.__might_label = Label(
			text=might_text, 
			x=position[0], 
			y=position[1] - 25, 
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
			Assets().custom['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['might_index'], 
			y=position[1] - 25,
			batch=batch,
			group=highlight_group
		)

		sanity_text = 'SAN: '
		for value in entry['sanity']:
			sanity_text += f'{value} '
		self.__sanity_label = Label(
			text=sanity_text, 
			x=position[0], 
			y=position[1] - 65, 
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
			Assets().custom['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['sanity_index'], 
			y=position[1] - 65,
			batch=batch,
			group=highlight_group
		)

		knowledge_text = 'KNW: '
		for value in entry['knowledge']:
			knowledge_text += f'{value} '
		self.__knowledge_label = Label(
			text=knowledge_text, 
			x=position[0], 
			y=position[1] - 105, 
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
			Assets().custom['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['knowledge_index'], 
			y=position[1] - 105,
			batch=batch,
			group=highlight_group
		)

		if not active:
			self.__active_label = Label(
				text='NOT ACTIVE', 
				x=position[0], 
				y=position[1] + 215, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=12, 
				color=(0, 0, 0, 255), 
				batch=batch,
				group=text_group
			)