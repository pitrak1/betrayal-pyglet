import pyglet
from src.server import server_room
from src.shared import constants, bounds, command

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ClientRoom(server_room.ServerRoom):
	def __init__(self, entry):
		super().__init__(entry)
		self.__selected = False
		self.__players = []

	def add_player(self, player):
		self.__players.append(player)
		self.__adjust_player_positions()

	def __adjust_player_positions(self):
		for i in range(len(self.__players)):
			player = self.__players[i]
			if len(self.__players) == 1:
				player.set_position(
					self._grid_x, 
					self._grid_y,
					self._grid_x * constants.GRID_SIZE, 
					self._grid_y * constants.GRID_SIZE,
					1.0
				)
			elif len(self.__players) == 2:
				player.set_position(
					self._grid_x, 
					self._grid_y,
					self._grid_x * constants.GRID_SIZE - 100 + 200 * i, 
					self._grid_y * constants.GRID_SIZE,
					1.0
				)
			else:
				player.set_position(
					self._grid_x, 
					self._grid_y,
					self._grid_x * constants.GRID_SIZE - 100 + 200 * (i % 2), 
					self._grid_y * constants.GRID_SIZE - 100 + 200 * (i // 2),
					1.0
				)

	def client_redraw_handler(self, command, state=None):
		self.__sprite = pyglet.sprite.Sprite(
			command.data['asset_manager'].rooms[self.asset_index],
			x=self._grid_x * constants.GRID_SIZE, 
			y=self._grid_y * constants.GRID_SIZE,
			batch=command.data['batch'],
			group=command.data['groups'][constants.ROOMS_GROUP]
		)
		self.__sprite.update(rotation=90 * self.sprite_rotation)

		self.__door_sprites = []
		for i in range(4):
			door_position = self.__get_door_position(self._grid_x, self._grid_y, i)
			door_sprite = pyglet.sprite.Sprite(
				command.data['asset_manager'].common['door'],
				x=door_position['x'],
				y=door_position['y'],
				batch=command.data['batch'], 
				group=command.data['groups'][constants.CHARACTERS_AND_DOORS_GROUP]
			)
			door_sprite.update(rotation=90 * i)
			self.__door_sprites.append(door_sprite)

		self.__label = pyglet.text.Label(
			self.display_name, 
			x=self._grid_x * constants.GRID_SIZE, 
			y=self._grid_y * constants.GRID_SIZE,
			batch=command.data['batch'], 
			group=command.data['groups'][constants.HIGHLIGHTS_GROUP]
		)

		if self.__selected:
			self.__selected_sprite = pyglet.sprite.Sprite(command.data['asset_manager'].common['room_selected'], batch=command.data['batch'], group=command.data['groups'][constants.HIGHLIGHTS_GROUP])

		return self.default_handler(command, state)

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

	# def client_translated_mouse_press_handler(self, command, state):
	# 	if self.within_bounds(command.data['x'], command.data['y']):
	# 		if command.data['button'] == pyglet.window.mouse.LEFT:
	# 			if not self.default_handler(command, state):
	# 				state.select(self)
	# 			return True
			# elif command.data['button'] == window.mouse.RIGHT and state.name('SelectedState'):
			# 	if not self.default_handler(command, state):
			# 		state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	# def client_select_handler(self, command, state):
	# 	self.selected = command.data['selected'] == self
	# 	self.default_handler(command, state)

	# def within_bounds(self, x, y):
	# 	return bounds.within_square_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.GRID_SIZE)

	def default_handler(self, command, state):
		return any(player.on_command(command, state) for player in self.__players)
