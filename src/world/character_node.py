from pyglet import sprite, window
from src.commands import commands
from src import character_tile

CHARACTER_SIZE = 150

class CharacterNode():
	def __init__(self, character_tile, grid_x, grid_y, state_machine):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.character_tile = character_tile
		self.character_tile.set_position(grid_x, grid_y)
		self.state_machine = state_machine

	def on_draw(self):
		self.character_tile.on_draw(self.state_machine.is_selected(self))

	def on_command(self, command):
		if isinstance(command, commands.MousePressCommand):
			return self.__mouse_press_handler(command)

	def __mouse_press_handler(self, command):
		if command.button == window.mouse.LEFT:
			if self.character_tile.within_bounds(command.x, command.y):
				self.state_machine.select(self)
				return True
			return False
		elif command.button == window.mouse.RIGHT:
			pass

	def on_update(self, dt):
		pass

	
