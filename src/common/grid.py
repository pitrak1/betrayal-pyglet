import pyglet
from lattice2d.grid import Tile, TileGrid, get_direction, get_distance, reverse_direction, UP, RIGHT, DOWN, LEFT
from lattice2d.client import Assets
from constants import Constants

class EmptyRoom(Tile):
	def __init__(self, state_machine, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(state_machine, grid_position, base_position)
		self.state_machine = state_machine
		self.add_command = state_machine.add_command
		self.doors = [True, True, True, True]
		self.links = []

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			if command.data['button'] == pyglet.window.mouse.RIGHT:
				print('something')


class Room(EmptyRoom):
	def __init__(self, state_machine, entry, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(state_machine, grid_position, base_position)
		self.entry = entry
		self.display_name = entry['display_name']
		self.key = entry['key']
		self.asset_index = entry['asset_index']
		self.doors = entry['doors']
		self.floor = entry['floor']
		self.sprite_rotation = entry['sprite_rotation']
		self.players = []
		self.links = []

		self.selected = False

		scaled_position = self.get_scaled_position()
		self.room_sprite = pyglet.sprite.Sprite(
			Assets()[self.entry['key']],
			x=scaled_position[0],
			y=scaled_position[1]
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90, scale=self.base_scale)


		self.door_sprites = []
		if self.doors[UP]:
			scaled_position = self.get_scaled_position((0, 0.5), (0, -20))
			door_sprite = pyglet.sprite.Sprite(
				Assets()['door'],
				x=scaled_position[0],
				y=scaled_position[1]
			)
			door_sprite.update(scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[RIGHT]:
			scaled_position = self.get_scaled_position((0.5, 0), (-20, 0))
			door_sprite = pyglet.sprite.Sprite(
				Assets()['door'],
				x=scaled_position[0],
				y=scaled_position[1]
			)
			door_sprite.update(rotation=90, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[DOWN]:
			scaled_position = self.get_scaled_position((0, -0.5), (0, 20))
			door_sprite = pyglet.sprite.Sprite(
				Assets()['door'],
				x=scaled_position[0],
				y=scaled_position[1]
			)
			door_sprite.update(rotation=180, scale=self.base_scale)
			self.door_sprites.append(door_sprite)

		if self.doors[LEFT]:
			scaled_position = self.get_scaled_position((-0.5, 0), (20, 0))
			door_sprite = pyglet.sprite.Sprite(
				Assets()['door'],
				x=scaled_position[0],
				y=scaled_position[1]
			)
			door_sprite.update(rotation=270, scale=self.base_scale)
			self.door_sprites.append(door_sprite)


	def register(self, layer):
		self.room_sprite.batch = layer.batch
		self.room_sprite.group = layer.groups[0]

		for door in self.door_sprites:
			door.batch = layer.batch
			door.group = layer.groups[1]

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


class RoomGrid(TileGrid):
	def __init__(self, state_machine, grid_dimensions):
		super().__init__(state_machine, grid_dimensions)
		self.children = []
		self.state_machine = state_machine
		self.add_command = state_machine.add_command
		for room in Constants.starting_rooms:
			self.add_tile(room['grid_position'], Room(state_machine, room, room['grid_position'], self.base_position))

	def add_tile(self, grid_position, tile):
		super().add_tile(grid_position, tile)
		self.state_machine.current_state.register_component(tile.key, 'environment', tile)

	def add_adjacent_links(self, start_tile, end_tile):
		if isinstance(end_tile, Tile):
			direction = get_direction(start_tile.grid_position, end_tile.grid_position)
			if start_tile.doors[direction] and end_tile.doors[reverse_direction(direction)]:
				start_tile.links.append(end_tile)
				end_tile.links.append(start_tile)
