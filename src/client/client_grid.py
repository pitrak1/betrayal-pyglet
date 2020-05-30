import pyglet
from lattice2d.grid import UP, RIGHT, LEFT, DOWN
from lattice2d.utilities.bounds import within_circle_bounds, within_square_bounds
from src.client.asset_manager import Assets
from src.common.grid import Room, RoomGrid, Player
from src.common import constants
import config

class ClientPlayer(Player):
	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.player_sprite = pyglet.sprite.Sprite(
			Assets().characters[self.variable_name],
			x=self.get_scaled_x_position(self.grid_x, 0),
			y=self.get_scaled_y_position(self.grid_y, 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(2)
		)
		self.player_sprite.update(scale=self.base_scale)

	def mouse_press_handler(self, command):
		if self.within_bounds(command.data['x'], command.data['y']):
			print(self.display_name)
			return True
		else:
			return False

	def within_bounds(self, x, y):
		return within_circle_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.CHARACTER_SIZE // 2)

class ClientRoom(Room):
	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.room_sprite = pyglet.sprite.Sprite(
			Assets().rooms[self.asset_index],
			x=self.get_scaled_x_position(self.grid_x, 0),
			y=self.get_scaled_y_position(self.grid_y, 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(1)
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90, scale=self.base_scale)

		self.door_sprites = []
		if self.doors[UP]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_x, 0),
				y=self.get_scaled_y_position(self.grid_y + 0.5, -20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[RIGHT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_x + 0.5, -20),
				y=self.get_scaled_y_position(self.grid_y, 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=90, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[DOWN]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_x, 0),
				y=self.get_scaled_y_position(self.grid_y - 0.5, 20),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=180, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[LEFT]:
			door_sprite = pyglet.sprite.Sprite(
				Assets().common['door'],
				x=self.get_scaled_x_position(self.grid_x - 0.5, 20),
				y=self.get_scaled_y_position(self.grid_y, 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(2)
			)
			door_sprite.update(rotation=270, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		self.other = [self.room_sprite] + self.door_sprites
		self.default_handler(command)

	def within_bounds(self, x, y):
		return within_square_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.GRID_SIZE)

	def mouse_press_handler(self, command):
		if self.within_bounds(command.data['x'], command.data['y']):
			if not self.default_handler(command):
				print(self.display_name)

class ClientRoomGrid(RoomGrid):
	def __init__(self):
		super().__init__()
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], ClientRoom(room, base_x=self.base_x, base_y=self.base_y))

	def add_actor(self, grid_x, grid_y, actor):
		super().add_actor(grid_x, grid_y, actor)
		actor.base_x = self.base_x
		actor.base_y = self.base_y
