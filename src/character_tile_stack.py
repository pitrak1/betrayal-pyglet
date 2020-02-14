from src import character_tile
import random

class CharacterTileStack():
	def __init__(self, images):
		self.images = images
		self.stack = []
		self.__create_character_tiles()
		random.shuffle(self.stack)

	def __create_character_tiles(self):
		self.stack.append(character_tile.CharacterTile(self.images, 'Brandon Jaspers', 'brandon_jaspers'))
		self.stack.append(character_tile.CharacterTile(self.images, 'Father Rhinehardt', 'father_rhinehardt'))

	def get_by_name(self, name):
		character = [x for x in self.stack if x.name == name]
		if len(character):
			self.stack.remove(character[0])
			return character[0]