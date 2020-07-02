import pyglet
from lattice2d.grid import UP, RIGHT, LEFT, DOWN, ScaledEmptyTile
from lattice2d.utilities.bounds import within_circle_bounds, within_square_bounds
from lattice2d.nodes import Command
from lattice2d.assets import Assets
from src.common.grid import Room, RoomGrid
from lattice2d.full.common import Player
from src.common import constants
import config

class ClientPlayer(Player):
	def __init__(self, name, add_command, connection=None, game=None, entry=None, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(name, connection, game, entry, grid_position, base_position)
		self.add_command = add_command
		self.selected = False

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.player_sprite = pyglet.sprite.Sprite(
			Assets().characters[self.variable_name],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(2)
		)
		self.player_sprite.update(scale=self.base_scale)
		if self.selected:
			self.player_highlight_sprite = pyglet.sprite.Sprite(
				Assets().common['character_selected'],
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
			(self.grid_position[0] * constants.GRID_SIZE, self.grid_position[1] * constants.GRID_SIZE), 
			position, 
			constants.CHARACTER_SIZE // 2
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
			Assets().rooms[self.asset_index],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(1)
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90, scale=self.base_scale)
		if self.selected:
			self.room_highlight_sprite = pyglet.sprite.Sprite(
				Assets().common['room_selected'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			self.room_highlight_sprite.update(scale=self.base_scale)

		self.door_sprites = []
		if self.doors[UP]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1] + 0.5, -20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[RIGHT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_position[0] + 0.5, -20),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=90, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[DOWN]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1] - 0.5, 20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=180, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[LEFT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
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
			(self.grid_position[0] * constants.GRID_SIZE, self.grid_position[1] * constants.GRID_SIZE), 
			position, 
			constants.GRID_SIZE
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

class ClientEmptyTile(ScaledEmptyTile):
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
			(self.grid_position[0] * constants.GRID_SIZE, self.grid_position[1] * constants.GRID_SIZE), 
			position, 
			constants.GRID_SIZE
		)


class ClientRoomGrid(RoomGrid):
	def __init__(self, add_command):
		super().__init__()
		self.children = []
		self.add_command = add_command
		for i in range(self.grid_dimensions[0] * self.grid_dimensions[1]):
			self.children.append(ClientEmptyTile(add_command, ((i % self.grid_dimensions[0]), (i // self.grid_dimensions[1])), self.base_position))
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_position'], ClientRoom(room, add_command, base_position=self.base_position))

	def add_actor(self, grid_position, actor):
		super().add_actor(grid_position, actor)
		actor.base_position = self.base_position
