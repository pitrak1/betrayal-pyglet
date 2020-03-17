import pyglet
from src.server import server_room as server_room_module
from src.shared import constants, bounds

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ClientRoom(server_room_module.ServerRoom):
	def __init__(self, entry, asset_manager):
		super().__init__(entry)
		self.sprite = pyglet.sprite.Sprite(asset_manager.rooms[entry['asset_index']])
		self.sprite.update(rotation=90 * self.sprite_rotation)
		self.door_sprites = [
			pyglet.sprite.Sprite(asset_manager.common['door']),
			pyglet.sprite.Sprite(asset_manager.common['door']), 
			pyglet.sprite.Sprite(asset_manager.common['door']), 
			pyglet.sprite.Sprite(asset_manager.common['door'])
		]
		self.label = pyglet.text.Label(entry['display_name'])
		self.selected_sprite = pyglet.sprite.Sprite(asset_manager.common['room_selected'])
		self.selected = False

	def set_position(self, grid_x, grid_y):
		super().set_position(grid_x, grid_y)
		self.sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)
		self.selected_sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)

		self.label.x = grid_x * constants.GRID_SIZE
		self.label.y = grid_y * constants.GRID_SIZE

		for i in range(4):
			door_position = self.__get_door_position(grid_x, grid_y, i)
			self.door_sprites[i].update(x=door_position['x'], y=door_position['y'], rotation=90 * i)

	def __get_door_position(self, grid_x, grid_y, direction):
		offset = (constants.GRID_SIZE // 2 - constants.DOOR_OFFSET)
		if direction == constants.UP:
			return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE + offset }
		elif direction == constants.RIGHT:
			return { 'x': grid_x * constants.GRID_SIZE + offset, 'y': grid_y * constants.GRID_SIZE }
		elif direction == constants.DOWN:
			return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE - offset }
		else:
			return { 'x': grid_x * constants.GRID_SIZE - offset, 'y': grid_y * constants.GRID_SIZE }

	def client_translated_mouse_press_handler(self, command, state):
		if self.within_bounds(command.data['x'], command.data['y']):
			if command.data['button'] == pyglet.window.mouse.LEFT:
				if not self.default_handler(command, state):
					state.select(self)
				return True
			# elif command.data['button'] == window.mouse.RIGHT and state.name('SelectedState'):
			# 	if not self.default_handler(command, state):
			# 		state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	def client_select_handler(self, command, state):
		self.selected = command.data['selected'] == self
		self.default_handler(command, state)

	def within_bounds(self, x, y):
		return bounds.within_square_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.GRID_SIZE)

	def default_handler(self, command, state):
		return any(player.on_command(command, state) for player in self.players)

	def draw(self):
		self.sprite.draw()
		if self.selected: self.selected_sprite.draw()
		self.label.draw()

		for i in range(4):
			if self.doors[i]: self.door_sprites[i].draw()

		for player in self.players:
			player.draw()
