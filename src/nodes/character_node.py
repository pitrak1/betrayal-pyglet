from pyglet import window
from src.nodes import visible_node

CHARACTER_SIZE = 150

class CharacterNode(visible_node.VisibleNode):
	def mouse_press_handler(self, command):
		if self.state_machine.current_state.__class__.__name__ != 'RotatingRoomState':
			if command.button == window.mouse.LEFT:
				if self.tile.within_bounds(command.position):
					self.state_machine.select(self)
					return True
				return False
			elif command.button == window.mouse.RIGHT:
				pass

	def default_handler(self, command):
		pass

	def on_update(self, dt):
		pass

	
