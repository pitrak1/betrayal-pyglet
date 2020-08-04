import pyglet
from lattice2d.grid.grid_navigation import UP, RIGHT, LEFT, DOWN
from lattice2d.utilities.bounds import within_square_bounds
from lattice2d.nodes.command import Command
from lattice2d.client.assets import Assets
from src.common.grid import Room
from constants import GRID_SIZE

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
				Austom().custom['room_selected'],
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
			(self.grid_position[0] * GRID_SIZE, self.grid_position[1] * GRID_SIZE), 
			position, 
			GRID_SIZE
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