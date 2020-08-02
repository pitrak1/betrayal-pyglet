from lattice2d.grid.player import Player as Lattice2dPlayer

class Player(Lattice2dPlayer):
	def set_character(self, character_entry):
		self.character_entry = character_entry
