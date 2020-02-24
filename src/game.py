import pyglet
from src.assets import asset_manager as asset_manager_module
from src.tiles import room_tile_stack as room_tile_stack_module, character_tile_stack as character_tile_stack_module
from src.states import state_machine as state_machine_module, commands as commands_module
from src.camera import camera as camera_module
from src.world import room_grid as room_grid_module

from pyglet.window import key

class Game():
	def __init__(self, window):
		self.window = window

		self.asset_manager = asset_manager_module.AssetManager()
		self.room_stack = room_tile_stack_module.RoomTileStack(self.asset_manager.rooms, self.asset_manager.misc)
		self.character_stack = character_tile_stack_module.CharacterTileStack(self.asset_manager.characters, self.asset_manager.misc)
		self.room_grid = room_grid_module.RoomGrid()
		self.camera = camera_module.Camera()
		
		self.command_queue = []
		self.state_machine = state_machine_module.StateMachine(self.command_queue)
		self.key_handler = pyglet.window.key.KeyStateHandler()
		window.push_handlers(self.key_handler)

		self.command_queue.append(commands_module.PlaceRoom(self.room_stack.get_by_name('Entrance Hall'), 10, 10, 1))
		self.command_queue.append(commands_module.PlaceRoom(self.room_stack.get_by_name('Foyer'), 10, 11, 0))
		self.command_queue.append(commands_module.PlaceRoom(self.room_stack.get_by_name('Grand Staircase'), 10, 12, 2))
		self.command_queue.append(commands_module.PlaceCharacter(self.character_stack.draw(), 10, 10))

	def on_draw(self):
		self.window.clear()
		self.camera.on_draw(self.state_machine.current_state)
		self.room_grid.on_draw(self.state_machine.current_state)

	def on_key_press(self, symbol, modifiers):
		self.command_queue.append(commands_module.KeyPress(symbol, modifiers))

	def on_mouse_press(self, x, y, button, modifiers):
		self.command_queue.append(commands_module.RawMousePress(x, y, button, modifiers))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.command_queue.append(commands_module.MouseScroll(x, y, dx, dy))

	def on_update(self, dt):
		while self.command_queue:
			command = self.command_queue.pop(0)
			self.asset_manager.on_command(command, self.state_machine.current_state)
			self.room_stack.on_command(command, self.state_machine.current_state)
			self.character_stack.on_command(command, self.state_machine.current_state)
			self.room_grid.on_command(command, self.state_machine.current_state)
			self.camera.on_command(command, self.state_machine.current_state)

		self.room_grid.on_update(dt, self.state_machine.current_state)
		self.camera.on_update(dt, self.state_machine.current_state, self.key_handler)

	def default_handler(self, command, state):
		pass
