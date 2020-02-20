from pyglet import window
from src.nodes import visible_node
from src.states import no_selection_state as no_selection_state_module, selected_state as selected_state_module

CHARACTER_SIZE = 150

class CharacterNode(visible_node.VisibleNode):
	def mouse_press_handler(self, command, state):
		if state.__class__ == no_selection_state_module.NoSelectionState or state.__class__ == selected_state_module.SelectedState:
			if command.button == window.mouse.LEFT:
				if self.tile.within_bounds(command.position):
					state.select(self)
					return True
				return False

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass

	
