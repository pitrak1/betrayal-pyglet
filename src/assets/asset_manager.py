import pyglet
from src import node as node_module

class AssetManager(node_module.Node):
	def __init__(self):
		self.__load_images()
		self.__center_images()

	def __load_images(self):
		pyglet.resource.path = ['assets']
		pyglet.resource.reindex()

		self.images = {}
		# self.images['blue_characters'] = pyglet.resource.image('blue_characters.jpg')
		self.images['brandon_jaspers'] = pyglet.resource.image('brandon_jaspers.png')
		self.images['darrin_williams'] = pyglet.resource.image('darrin_williams.png')
		entrance = pyglet.resource.image('entrance.jpg')
		self.images['rooms'] = list(pyglet.image.ImageGrid(entrance, 3, 1))
		rooms = pyglet.resource.image('rooms.jpg')
		self.images['rooms'] = self.images['rooms'] + list(pyglet.image.ImageGrid(rooms, 8, 8))
		self.images['event'] = pyglet.resource.image('event.jpg')
		# self.images['event_cards'] = pyglet.resource.image('event_cards.jpg')
		self.images['father_rhinehardt'] = pyglet.resource.image('father_rhinehardt.png')
		# self.images['green_characters'] = pyglet.resource.image('green_characters.jpg')
		self.images['heather_granville'] = pyglet.resource.image('heather_granville.png')
		self.images['item'] = pyglet.resource.image('item.jpg')
		# self.images['item_cards'] = pyglet.resource.image('item_cards.jpg')
		self.images['jenny_leclerc'] = pyglet.resource.image('jenny_leclerc.png')
		self.images['madame_zostra'] = pyglet.resource.image('madame_zostra.png')
		self.images['missy_dubourde'] = pyglet.resource.image('missy_dubourde.png')
		self.images['omen'] = pyglet.resource.image('omen.jpg')
		# self.images['omen_cards'] = pyglet.resource.image('omen_cards.jpg')
		self.images['ox_bellows'] = pyglet.resource.image('ox_bellows.png')
		self.images['peter_akimoto'] = pyglet.resource.image('peter_akimoto.png')
		self.images['professor_longfellow'] = pyglet.resource.image('professor_longfellow.png')
		# self.images['purple_characters'] = pyglet.resource.image('purple_characters.jpg')
		# self.images['red_characters'] = pyglet.resource.image('red_characters.jpg')
		self.images['vivian_lopez'] = pyglet.resource.image('vivian_lopez.png')
		# self.images['white_characters'] = pyglet.resource.image('white_characters.jpg')
		# self.images['yellow_characters'] = pyglet.resource.image('yellow_characters.jpg')
		self.images['zoe_ingstrom'] = pyglet.resource.image('zoe_ingstrom.png')
		self.images['door'] = pyglet.resource.image('door.png')
		self.images['room_selected'] = pyglet.resource.image('room_selected.png')
		self.images['character_selected'] = pyglet.resource.image('character_selected.png')

	def __center_images(self):
		for key, value in self.images.items():
			if value.__class__.__name__ == 'ImageGrid' or value.__class__.__name__ == 'list':
				for image in value:
					self.__center_image(image)
			else:
				self.__center_image(value)

	def __center_image(self, image):
	    image.anchor_x = image.width / 2
	    image.anchor_y = image.height / 2
