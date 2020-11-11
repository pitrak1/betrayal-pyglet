import pyglet
from lattice2d.components import Area, Label, Component
from lattice2d.client import Assets
from lattice2d.nodes import Node
from lattice2d.command import Command
from lattice2d.grid import GridEntity, UP, RIGHT, LEFT, DOWN
from lattice2d.utilities import within_square_bounds, within_circle_bounds
from src.common.grid import Room, RoomGrid
from src.common.player import Player
from constants import Constants

class GameListing(Component):
	def __init__(self, name, players, position, on_click):
		super().__init__()
		self.__area = Area(
			position=position,
			unit_dimensions=(13, 2),
			align='left'
		)
		self.__game_name = Label(
			text=name,
			x=position[0],
			y=position[1],
			anchor_x='left',
			anchor_y='center',
			align='left',
			font_size=15,
			color=(0, 0, 0, 255)
		)
		self.__player_count = Label(
			text=f'{players}/{Constants.max_players_per_game}',
			x=position[0] + 390,
			y=position[1],
			anchor_x='right',
			anchor_y='center',
			align='right',
			font_size=15,
			color=(0, 0, 0, 255)
		)
		self.on_click = on_click

	def register(self, layer):
		self.__area.register(layer)
		self.__game_name.register(layer)
		self.__player_count.register(layer)

	def mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds((command.data['x'], command.data['y'])):
			self.on_click()

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


class CharacterTile(Component):
	def __init__(self, entry, position, active):
		super().__init__()
		self.display_name = entry['display_name']
		self.active = active
		self.__area = Area(
			position=(position[0], position[1] + 60), 
			unit_dimensions=(8, 12)
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
			color=(0, 0, 0, 255)
		)
		self.__picture = pyglet.sprite.Sprite(
			Assets()[entry['key']], 
			x=position[0], 
			y=position[1] + 120
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
			color=(0, 0, 0, 255)
		)
		self.__speed_indicator = pyglet.sprite.Sprite(
			Assets()['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['speed_index'], 
			y=position[1] + 15
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
			color=(0, 0, 0, 255)
		)
		self.__might_indicator = pyglet.sprite.Sprite(
			Assets()['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['might_index'], 
			y=position[1] - 25
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
			color=(0, 0, 0, 255)
		)
		self.__sanity_indicator = pyglet.sprite.Sprite(
			Assets()['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['sanity_index'], 
			y=position[1] - 65
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
			color=(0, 0, 0, 255)
		)
		self.__knowledge_indicator = pyglet.sprite.Sprite(
			Assets()['attribute_highlight'], 
			x=position[0] - 60 + 20 * entry['knowledge_index'], 
			y=position[1] - 105
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
				color=(0, 0, 0, 255)
			)

	def register(self, layer):
		self.__area.register(layer)
		self.__name_label.register(layer, 1)
		self.__picture.batch = layer.batch
		self.__picture.group = layer.groups[1]

		self.__speed_label.register(layer, 1)
		self.__speed_indicator.batch = layer.batch
		self.__speed_indicator.group = layer.groups[2]

		self.__might_label.register(layer, 1)
		self.__might_indicator.batch = layer.batch
		self.__might_indicator.group = layer.groups[2]

		self.__knowledge_label.register(layer, 1)
		self.__knowledge_indicator.batch = layer.batch
		self.__knowledge_indicator.group = layer.groups[2]

		self.__sanity_label.register(layer, 1)
		self.__sanity_indicator.batch = layer.batch
		self.__sanity_indicator.group = layer.groups[2]

		if not self.active:
			self.__active_label.register(layer, 1)
