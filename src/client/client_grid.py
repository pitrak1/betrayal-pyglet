import pyglet
from lattice2d.grid import UP, RIGHT, LEFT, DOWN
from src.client.asset_manager import Assets
from src.common.grid import Room, RoomGrid
from src.common import constants
import config

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

class ClientRoomGrid(RoomGrid):
	def __init__(self):
		super().__init__()
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], ClientRoom(room, base_x=self.base_x, base_y=self.base_y))
