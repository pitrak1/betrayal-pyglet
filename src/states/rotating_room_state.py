from src.states import state as state_module, no_selection_state as no_selection_state_module

class RotatingRoomState(state_module.State):
	def __init__(self, state_machine, grid_position, entering_direction):
		super().__init__(state_machine)
		self.grid_position = grid_position
		self.entering_direction = entering_direction

	def is_rotating(self, grid_position):
		return self.grid_position == grid_position

	def place_room(self):
		self.state_machine.current_state = no_selection_state_module.NoSelectionState(self.state_machine)