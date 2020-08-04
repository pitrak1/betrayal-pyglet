import pyglet
from lattice2d.utilities.bounds import within_circle_bounds
from lattice2d.nodes.command import Command
from lattice2d.client.assets import Assets
from src.common.player import Player
from constants import GRID_SIZE, CHARACTER_SIZE

class ClientPlayer(Player):
	def __init__(self, name, connection=None, game=None, grid_position=(None, None), base_position=(0, 0), add_command=None, character_entry=None):
		super().__init__(name, connection, game, grid_position, base_position, add_command, character_entry)
		self.selected = False

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.player_sprite = pyglet.sprite.Sprite(
			Assets().characters[self.character_entry['variable_name']],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(2)
		)
		self.player_sprite.update(scale=self.base_scale)
		if self.selected:
			self.player_highlight_sprite = pyglet.sprite.Sprite(
				Assets().custom['character_selected'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(3)
			)
			self.player_highlight_sprite.update(scale=self.base_scale)

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			self.add_command(Command('client_select', { 'selected': self }))
			self.add_command(Command('redraw'))
			return True
		else:
			return False

	def within_bounds(self, position):
		return within_circle_bounds(
			(self.grid_position[0] * GRID_SIZE, self.grid_position[1] * GRID_SIZE), 
			position, 
			CHARACTER_SIZE // 2
		)

	def client_select_handler(self, command):
		self.selected = command.data['selected'] == self