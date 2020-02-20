from src.states import state as state_module, rotating_room_state as rotating_room_state_module, commands as commands_module

class SelectedState(state_module.State):
	def __init__(self, state_machine, selected):
		super().__init__(state_machine)
		self.selected = selected

	def select(self, selected):
		self.selected = selected

	def is_selected(self, node):
		return self.selected == node

	def move(self, grid_position):
		self.state_machine.command_queue.append(commands_module.MoveCharacterCommand(self.selected, grid_position))

	def move_into_new_room(self, grid_position, direction):
		self.state_machine.command_queue.append(commands_module.AddRoomCommand(self.state_machine.room_stack.draw(), grid_position, 0))
		self.state_machine.command_queue.append(commands_module.MoveCharacterCommand(self.selected, grid_position))
		self.state_machine.current_state = rotating_room_state_module.RotatingRoomState(self.state_machine, grid_position, direction)