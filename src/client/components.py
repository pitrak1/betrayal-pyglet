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

class ClientEmptyTile(GridEntity):
	def __init__(self, add_command, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(grid_position, base_position)
		self.add_command = add_command

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			if command.data['button'] == pyglet.window.mouse.RIGHT:
				print('something')
				# self.add_command(Command('client_move', { 'grid_x': self.grid_x, 'grid_y': self.grid_y }))

	def within_bounds(self, position):
		return within_square_bounds(
			(self.grid_position[0] * Constants.grid_size, self.grid_position[1] * Constants.grid_size), 
			position, 
			Constants.grid_size
		)

class ClientPlayer(Player):
	def __init__(self, name, connection=None, game=None, grid_position=(None, None), base_position=(0, 0), add_command=None, character_entry=None):
		super().__init__(name, connection, game, grid_position, base_position, add_command, character_entry)
		self.selected = False

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.player_sprite = pyglet.sprite.Sprite(
			Assets().characters[self.character_entry['variable_name']],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(2)
		)
		self.player_sprite.update(scale=self.base_scale)
		if self.selected:
			self.player_highlight_sprite = pyglet.sprite.Sprite(
				Assets().custom['character_selected'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(3)
			)
			self.player_highlight_sprite.update(scale=self.base_scale)

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			self.add_command(Command('client_select', { 'selected': self }))
			self.add_command(Command('redraw'))
			return True
		else:
			return False

	def within_bounds(self, position):
		return within_circle_bounds(
			(self.grid_position[0] * Constants.grid_size, self.grid_position[1] * Constants.grid_size), 
			position, 
			Constants.character_size // 2
		)

	def client_select_handler(self, command):
		self.selected = command.data['selected'] == self


class ClientRoom(Room):
	def __init__(self, entry, add_command, base_position=(0, 0)):
		super().__init__(entry, base_position)
		self.add_command = add_command
		self.selected = False

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.room_sprite = pyglet.sprite.Sprite(
			Assets().tiles[self.entry['variable_name']],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(1)
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90, scale=self.base_scale)
		if self.selected:
			self.room_highlight_sprite = pyglet.sprite.Sprite(
				Assets().custom['room_selected'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			self.room_highlight_sprite.update(scale=self.base_scale)

		self.door_sprites = []
		if self.doors[UP]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().custom['door'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1] + 0.5, -20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[RIGHT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().custom['door'],
				x=self.get_scaled_x_position(self.grid_position[0] + 0.5, -20),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=90, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[DOWN]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().custom['door'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1] - 0.5, 20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=180, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[LEFT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().custom['door'],
				x=self.get_scaled_x_position(self.grid_position[0] - 0.5, 20),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=270, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		self.other = [self.room_sprite] + self.door_sprites
		self.default_handler(command)

	def within_bounds(self, position):
		return within_square_bounds(
			(self.grid_position[0] * Constants.grid_size, self.grid_position[1] * Constants.grid_size), 
			position, 
			Constants.grid_size
		)

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			if command.data['button'] == pyglet.window.mouse.LEFT:
				if not self.default_handler(command):
					self.add_command(Command('client_select', { 'selected': self }))
					self.add_command(Command('redraw'))
			elif command.data['button'] == pyglet.window.mouse.RIGHT:
				self.add_command(Command('client_move', { 'grid_position': self.grid_position }))

	def client_select_handler(self, command):
		self.selected = command.data['selected'] == self
		self.default_handler(command)

class ClientRoomGrid(RoomGrid):
	def __init__(self, add_command, grid_dimensions):
		super().__init__(grid_dimensions)
		self.children = []
		self.add_command = add_command
		for i in range(self.grid_dimensions[0] * self.grid_dimensions[1]):
			self.children.append(ClientEmptyTile(add_command, ((i % self.grid_dimensions[0]), (i // self.grid_dimensions[1])), self.base_position))
		for room in Constants.starting_rooms:
			self.add_tile(room['grid_position'], ClientRoom(room, add_command, base_position=self.base_position))