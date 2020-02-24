from src.tiles import character_tile, tile_stack

class CharacterTileStack(tile_stack.TileStack):
	def create_tiles(self, images, misc):
		selected = misc['character_selected']
		self.stack.append(character_tile.CharacterTile('Brandon Jaspers', images['brandon_jaspers'], selected))
		self.stack.append(character_tile.CharacterTile('Father Rhinehardt', images['father_rhinehardt'], selected))

	def get_character_tile_handler(self, command, state):
		if command.name:
			state.set_character_tile(self.get_by_name(command.name))
		else:
			state.set_character_tile(self.draw())
