from src.tiles import character_tile, tile_stack

class CharacterTileStack(tile_stack.TileStack):
	def create_tiles(self, images):
		self.stack.append(character_tile.CharacterTile('Brandon Jaspers', images, 'brandon_jaspers'))
		self.stack.append(character_tile.CharacterTile('Father Rhinehardt', images, 'father_rhinehardt'))
