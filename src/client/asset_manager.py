import pyglet
import config

class AssetManager():
	def __init__(self):
		pyglet.resource.path = ['assets']
		pyglet.resource.reindex()

		self.__load_common()
		self.__load_characters()
		self.__load_rooms()

	def __load_common(self):
		self.common = {}
		brown_button = pyglet.resource.image('brown_button.png')
		self.common['brown_button'] = list(pyglet.image.ImageGrid(brown_button, 3, 3))
		grey_button = pyglet.resource.image('grey_button.png')
		self.common['grey_button'] = list(pyglet.image.ImageGrid(grey_button, 3, 3))
		white_button = pyglet.resource.image('white_button.png')
		self.common['white_button'] = list(pyglet.image.ImageGrid(white_button, 3, 3))
		self.common['crown'] = pyglet.resource.image('crown.png')
		self.common['menu_background'] = pyglet.resource.image('menu_background.jpg')
		self.common['door'] = pyglet.resource.image('door.png')
		self.common['room_selected'] = pyglet.resource.image('room_selected.png')
		self.common['character_selected'] = pyglet.resource.image('character_selected.png')
		self.common['attribute_highlight'] = pyglet.resource.image('attribute_highlight.png')

		for key, value in self.common.items():
			if isinstance(value, list):
				for sprite in value:
					self.__center_image(sprite)
			else:
				self.__center_image(value)

	def __load_characters(self):
		self.characters = {}
		for character in config.STARTING_CHARACTERS:
			self.characters[character['variable_name']] = pyglet.resource.image(character['portrait_asset'])
			self.__center_image(self.characters[character['variable_name']])

	def __load_rooms(self):
		rooms = pyglet.resource.image('rooms.jpg')
		self.rooms = list(pyglet.image.ImageGrid(rooms, 9, 8))

		for value in self.rooms:
			self.__center_image(value)

	def __center_image(self, image):
	    image.anchor_x = image.width / 2
	    image.anchor_y = image.height / 2
