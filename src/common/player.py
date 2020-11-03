from lattice2d.server import Player as Lattice2dPlayer

class Player(Lattice2dPlayer):
	def __init__(self, name, connection=None, game=None, grid_position=(None, None), base_position=(0, 0), add_command=None, character_entry=None):
		super().__init__(name, connection, game)
		self.add_command = add_command
		self.character_entry = character_entry

	def set_character(self, character_entry):
		self.character_entry = character_entry
