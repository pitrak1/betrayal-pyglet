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
		for key, value in config.COMMON_ASSETS.items():
			if value['asset_type'] == 'single':
				self.common[key] = pyglet.resource.image(value['asset'])
			else:
				image = pyglet.resource.image(value['asset'])
				self.common[key] = list(pyglet.image.ImageGrid(image, value['rows'], value['columns']))

		for key, value in self.common.items():
			if isinstance(value, list):
				for sprite in value:
					self.__center_image(sprite)
			else:
				self.__center_image(value)

	def __load_characters(self):
		self.characters = {}
		for character in config.CHARACTERS:
			self.characters[character['variable_name']] = pyglet.resource.image(character['portrait_asset'])
			self.__center_image(self.characters[character['variable_name']])

	def __load_rooms(self):
		rooms = pyglet.resource.image(config.ROOMS_ASSET['asset'])
		self.rooms = list(pyglet.image.ImageGrid(rooms, config.ROOMS_ASSET['rows'], config.ROOMS_ASSET['columns']))

		for value in self.rooms:
			self.__center_image(value)

	def __center_image(self, image):
	    image.anchor_x = image.width / 2
	    image.anchor_y = image.height / 2
