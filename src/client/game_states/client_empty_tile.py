import pyglet
from lattice2d.grid import GridEntity
from lattice2d.utilities import within_square_bounds
from constants import GRID_SIZE

class ClientEmptyTile(GridEntity):
	def __init__(self, add_command, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(grid_position, base_position)
		self.add_command = add_command

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			if command.data['button'] == pyglet.window.mouse.RIGHT:
				print('something')
				# self.add_command(Command('client_move', { 'grid_x': self.grid_x, 'grid_y': self.grid_y }))

	def within_bounds(self, position):
		return within_square_bounds(
			(self.grid_position[0] * GRID_SIZE, self.grid_position[1] * GRID_SIZE), 
			position, 
			GRID_SIZE
		)