import pyglet

class AssetManager():
	def __init__(self):
		pyglet.resource.path = ['assets']
		pyglet.resource.reindex()

		self.__load_menu()
		self.__load_common()
		self.__load_characters()
		self.__load_rooms()
		self.__load_misc()

	def __load_menu(self):
		self.menu = {}
		self.menu['menu_background'] = pyglet.resource.image('menu_background.jpg')

		for key, value in self.menu.items():
			self.__center_image(value)

	def __load_common(self):
		self.common = {}
		brown_button = pyglet.resource.image('brown_button.png')
		self.common['brown_button'] = list(pyglet.image.ImageGrid(brown_button, 3, 3))
		grey_button = pyglet.resource.image('grey_button.png')
		self.common['grey_button'] = list(pyglet.image.ImageGrid(grey_button, 3, 3))
		white_button = pyglet.resource.image('white_button.png')
		self.common['white_button'] = list(pyglet.image.ImageGrid(white_button, 3, 3))
		self.common['crown'] = pyglet.resource.image('crown.png')

		for key, value in self.common.items():
			if isinstance(value, list):
				for sprite in value:
					self.__center_image(sprite)
			else:
				self.__center_image(value)

	def __load_characters(self):
		self.characters = {}
		self.characters['brandon_jaspers'] = pyglet.resource.image('brandon_jaspers.png')
		self.characters['darrin_williams'] = pyglet.resource.image('darrin_williams.png')
		self.characters['father_rhinehardt'] = pyglet.resource.image('father_rhinehardt.png')
		self.characters['heather_granville'] = pyglet.resource.image('heather_granville.png')
		self.characters['jenny_leclerc'] = pyglet.resource.image('jenny_leclerc.png')
		self.characters['madame_zostra'] = pyglet.resource.image('madame_zostra.png')
		self.characters['missy_dubourde'] = pyglet.resource.image('missy_dubourde.png')
		self.characters['ox_bellows'] = pyglet.resource.image('ox_bellows.png')
		self.characters['peter_akimoto'] = pyglet.resource.image('peter_akimoto.png')
		self.characters['professor_longfellow'] = pyglet.resource.image('professor_longfellow.png')
		self.characters['vivian_lopez'] = pyglet.resource.image('vivian_lopez.png')
		self.characters['zoe_ingstrom'] = pyglet.resource.image('zoe_ingstrom.png')

		for key, value in self.characters.items():
			self.__center_image(value)

	def __load_rooms(self):
		entrance = pyglet.resource.image('entrance.jpg')
		self.rooms = list(pyglet.image.ImageGrid(entrance, 3, 1))
		rooms = pyglet.resource.image('rooms.jpg')
		self.rooms = self.rooms + list(pyglet.image.ImageGrid(rooms, 8, 8))

		for value in self.rooms:
			self.__center_image(value)

	def __load_misc(self):
		self.misc = {}
		self.misc['door'] = pyglet.resource.image('door.png')
		self.misc['room_selected'] = pyglet.resource.image('room_selected.png')
		self.misc['character_selected'] = pyglet.resource.image('character_selected.png')
		self.misc['attribute_highlight'] = pyglet.resource.image('attribute_highlight.png')

		for key, value in self.misc.items():
			self.__center_image(value)

	def __center_image(self, image):
	    image.anchor_x = image.width / 2
	    image.anchor_y = image.height / 2
