import pyglet
from src.server import server_character as server_character_module

class ClientCharacter(server_character_module.ServerCharacter):
	def __init__(self, entry, asset_manager):
		super().__init__(entry)
		self.portrait_sprite = pyglet.sprite.Sprite(asset_manager.characters[self.variable_name])
		self.selected_sprite = pyglet.sprite.Sprite(asset_manager.common['character_selected'])
		self.selected = False

	def draw(self):
		self.portrait_sprite.draw()
		if self.selected: self.selected_sprite.draw()
