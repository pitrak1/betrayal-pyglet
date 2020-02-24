import pyglet
from src import node as node_module

class AssetManager(node_module.Node):
	def __init__(self):
		pyglet.resource.path = ['assets']
		pyglet.resource.reindex()

		self.__load_characters()
		self.__load_rooms()
		self.__load_misc()

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

		for key, value in self.misc.items():
			self.__center_image(value)

	def __center_image(self, image):
	    image.anchor_x = image.width / 2
	    image.anchor_y = image.height / 2

	def on_draw(self, state):
		pass

	def get_character_asset_handler(self, command, state):
		state.set_character_asset(self.characters[command.character_asset])

	def get_room_asset_handler(self, command, state):
		state.set_room_asset(self.rooms[command.room_index])

	def get_misc_asset_handler(self, command, state):
		state.set_misc_asset(self.misc[command.misc_asset])

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass
