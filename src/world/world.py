import pyglet
import assets

class World():
	def __init__(self):
		self.images = assets.load_images()

		self.rooms = [[0] * 30 for i in range(30)]
		self.room_batch = pyglet.graphics.Batch()

		self.characters = []
		self.character_batch = pyglet.graphics.Batch()

		self.add_room(1, 1, self.images['rooms'][0])
		self.add_character(1, 1, self.images['heather_granville'])

		
	def draw(self):
		self.room_batch.draw()
		self.character_batch.draw()

	def add_room(self, x, y, img):
		if (x < -15 or x > 14):
			raise 'Attempting to add room at x position ' + x
		if (y < -15 or y > 14):
			raise 'Attempting to add room at y position ' + y

		x_position = x * 512
		y_position = y * 512

		self.rooms[x + 15][y + 15] = pyglet.sprite.Sprite(img, x_position, y_position, batch=self.room_batch)

	def add_character(self, x, y, img):
		if (x < -15 or x > 14):
			raise 'Attempting to add character at x position ' + x
		if (y < -15 or y > 14):
			raise 'Attempting to add character at y position ' + y

		x_position = x * 512
		y_position = y * 512

		character = pyglet.sprite.Sprite(img, x_position, y_position, batch=self.character_batch)
		self.characters.append(character)






