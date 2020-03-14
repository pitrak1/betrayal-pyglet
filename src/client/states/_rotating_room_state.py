from src.states import state as state_module, no_selection_state as no_selection_state_module, commands as commands_module

class RotatingRoomState(state_module.State):
	def __init__(self, state_machine, grid_x, grid_y, entering_direction):
		super().__init__(state_machine)
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.entering_direction = entering_direction

	def is_rotating(self, grid_x, grid_y):
		return self.grid_x == grid_x and self.grid_y == grid_y

	def trigger_stop_room_rotating(self):
		self.waiting = ['set_room_rotation_valid']
		self.waiting_action = lambda : self.complete_stop_room_rotating()
		self.state_machine.command_queue.append(commands_module.GetRoomRotationValid(self.grid_x, self.grid_y, self.entering_direction))

	def set_room_rotation_valid(self, valid):
		self.room_rotation_valid = valid
		self.check_waiting('set_room_rotation_valid')

	def complete_stop_room_rotating(self):
		if self.room_rotation_valid:
			self.state_machine.current_state = no_selection_state_module.NoSelectionState(self.state_machine)
