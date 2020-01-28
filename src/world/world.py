import pyglet
from src import assets
from src.world import absolute_node, relative_node

MAP_WIDTH = 6
MAP_HEIGHT = 6
ROOM_SIZE = 512

class World():
	def __init__(self):
		self.images = assets.load_images()

		self.rooms = [[0] * MAP_WIDTH for i in range(MAP_HEIGHT)]
		self.room_batch = pyglet.graphics.Batch()

		self.characters = []
		self.character_batch = pyglet.graphics.Batch()

		self.add_room(1, 1, self.images['rooms'][0])
		self.add_room(1, 2, self.images['rooms'][1])
		self.add_character(1, 1, self.images['heather_granville'])

		
	def draw(self):
		self.room_batch.draw()
		self.character_batch.draw()

	def update(self, dt, event):
		for character in self.characters:
			print('character')
			# character.update(dt, event)

		for x in self.rooms:
			for y in x:
				print('room')
				# y.update(dt, event)

	def add_room(self, x, y, img):
		offset_x = x + MAP_WIDTH // 2
		offset_y = y + MAP_HEIGHT // 2

		if (offset_x < 0 or offset_x > MAP_WIDTH - 1):
			raise ValueError('Attempting to add room at x position ' + str(x))
		if (offset_y < 0 or offset_y > MAP_HEIGHT - 1):
			raise ValueError('Attempting to add room at y position ' + str(y))

		x_position = x * ROOM_SIZE
		y_position = y * ROOM_SIZE

		self.rooms[offset_x][offset_y] = absolute_node.AbsoluteNode(img, x = x_position, y = y_position, batch=self.room_batch)

	def add_character(self, x, y, img):
		offset_x = x + MAP_WIDTH // 2
		offset_y = y + MAP_HEIGHT // 2

		if (offset_x < 0 or offset_x > MAP_WIDTH - 1):
			raise ValueError('Attempting to add character at x position ' + str(x))
		if (offset_y < 0 or offset_y > MAP_HEIGHT - 1):
			raise ValueError('Attempting to add character at y position ' + str(y))

		x_position = x * ROOM_SIZE
		y_position = y * ROOM_SIZE

		character = relative_node.RelativeNode(img, batch=self.character_batch)
		self.characters.append(character)
		self.rooms[offset_x][offset_y].add_child(character)
		character.update_relative(x = 50, y = 50)






