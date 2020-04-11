import pyglet
from src.server import server_room
from src.common import constants, bounds, command, logger

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ClientRoom(server_room.ServerRoom):
	def __init__(self, entry, testing=False):
		super().__init__(entry)
		self.testing = testing
		self.selected = False

	def add_player(self, player):
		self.players.append(player)
		self.adjust_player_positions()

	def adjust_player_positions(self):
		for i in range(len(self.players)):
			player = self.players[i]
			if len(self.players) == 1:
				player.set_position(
					self.grid_x, 
					self.grid_y,
					self.grid_x * constants.GRID_SIZE, 
					self.grid_y * constants.GRID_SIZE,
					1.0
				)
			elif len(self.players) == 2:
				player.set_position(
					self.grid_x, 
					self.grid_y,
					self.grid_x * constants.GRID_SIZE - 100 + 200 * i, 
					self.grid_y * constants.GRID_SIZE,
					1.0
				)
			else:
				player.set_position(
					self.grid_x, 
					self.grid_y,
					self.grid_x * constants.GRID_SIZE - 100 + 200 * (i % 2), 
					self.grid_y * constants.GRID_SIZE - 100 + 200 * (i // 2),
					1.0
				)

	def redraw(self, command, state):
		if not self.testing:
			self.sprite = pyglet.sprite.Sprite(
				command.data['asset_manager'].rooms[self.asset_index],
				x=self.grid_x * constants.GRID_SIZE, 
				y=self.grid_y * constants.GRID_SIZE,
				batch=command.data['batch'],
				group=command.data['groups'][constants.ROOMS_GROUP]
			)
			self.sprite.update(rotation=90 * self.sprite_rotation)

			self.door_sprites = []
			for i in range(4):
				door_position = self.get_door_position(self.grid_x, self.grid_y, i)
				door_sprite = pyglet.sprite.Sprite(
					command.data['asset_manager'].common['door'],
					x=door_position['x'],
					y=door_position['y'],
					batch=command.data['batch'], 
					group=command.data['groups'][constants.CHARACTERS_AND_DOORS_GROUP]
				)
				door_sprite.update(rotation=90 * i)
				self.door_sprites.append(door_sprite)

			self.label = pyglet.text.Label(
				self.display_name, 
				x=self.grid_x * constants.GRID_SIZE, 
				y=self.grid_y * constants.GRID_SIZE,
				batch=command.data['batch'], 
				group=command.data['groups'][constants.HIGHLIGHTS_GROUP]
			)

			if self.selected:
				self.selected_sprite = pyglet.sprite.Sprite(
					command.data['asset_manager'].common['room_selected'], 
					x=self.grid_x * constants.GRID_SIZE, 
					y=self.grid_y * constants.GRID_SIZE,
					batch=command.data['batch'], 
					group=command.data['groups'][constants.HIGHLIGHTS_GROUP]
				)


	def client_redraw_handler(self, command, state=None):
		logger.log(f'Room {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		self.redraw(command, state)
		return self.default_handler(command, state)

	def get_door_position(self, grid_x, grid_y, direction):
		offset = (constants.GRID_SIZE // 2 - constants.DOOR_OFFSET)
		if direction == constants.UP:
			return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE + offset }
		elif direction == constants.RIGHT:
			return { 'x': grid_x * constants.GRID_SIZE + offset, 'y': grid_y * constants.GRID_SIZE }
		elif direction == constants.DOWN:
			return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE - offset }
		else:
			return { 'x': grid_x * constants.GRID_SIZE - offset, 'y': grid_y * constants.GRID_SIZE }

	def client_mouse_press_handler(self, command, state):
		logger.log(f'Room {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		if self.within_bounds(command.data['x'], command.data['y']):
			logger.log(f'Within bounds of Room {self.variable_name}', logger.LOG_LEVEL_DEBUG)
			if command.data['button'] == pyglet.window.mouse.LEFT:
				if not self.default_handler(command, state):
					logger.log(f'LMB not within bounds of players of Room {self.variable_name}, selecting', logger.LOG_LEVEL_DEBUG)
					state.select(self)
				return True
			elif command.data['button'] == pyglet.window.mouse.RIGHT:
				logger.log(f'RMB within bounds of Room {self.variable_name}, moving', logger.LOG_LEVEL_DEBUG)
				state.trigger_selected_character_move(self.grid_x, self.grid_y)

	def client_select_handler(self, command, state):
		logger.log(f'Room {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		self.selected = command.data['selected'] == self
		self.default_handler(command, state)

	def within_bounds(self, x, y):
		return bounds.within_square_bounds(
			self.grid_x * constants.GRID_SIZE, 
			self.grid_y * constants.GRID_SIZE, 
			x, 
			y, 
			constants.GRID_SIZE
		)

	def default_handler(self, command, state):
		return any(player.on_command(command, state) for player in self.players)
