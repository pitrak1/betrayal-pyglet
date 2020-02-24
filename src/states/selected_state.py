from src.states import state as state_module, rotating_room_state as rotating_room_state_module, commands as commands_module
from src.utils import grid as grid_module

class SelectedState(state_module.State):
	def __init__(self, state_machine, selected):
		super().__init__(state_machine)
		self.selected = selected

	def select(self, selected):
		self.selected = selected
		self.state_machine.command_queue.append(commands_module.Select(selected))

	def trigger_selected_character_move(self, end_x, end_y, is_room):
		self.waiting = ['set_selected_character_move_valid']
		self.waiting_action = lambda : self.complete_selected_character_move(end_x, end_y, is_room)
		self.state_machine.command_queue.append(commands_module.GetSelectedCharacterMoveValid(self.selected.grid_x, self.selected.grid_y, end_x, end_y))

	def set_selected_character_move_valid(self, valid):
		self.selected_character_move_valid = valid
		self.check_waiting('set_selected_character_move_valid')

	def complete_selected_character_move(self, end_x, end_y, is_room):
		if self.selected_character_move_valid:
			if is_room:
				self.state_machine.command_queue.append(commands_module.MoveCharacter(self.selected, end_x, end_y))
			else:
				direction = grid_module.get_direction(self.selected.grid_x, self.selected.grid_y, end_x, end_y)
				self.waiting = ['set_room_tile']
				def action():
					self.state_machine.command_queue.append(commands_module.PlaceRoom(self.room_tile, end_x, end_y, 0))
					self.state_machine.command_queue.append(commands_module.MoveCharacter(self.selected, end_x, end_y))
					self.state_machine.command_queue.append(commands_module.Select(None))
					self.state_machine.current_state = rotating_room_state_module.RotatingRoomState(self.state_machine, end_x, end_y, direction)
				self.waiting_action = action
				self.state_machine.command_queue.append(commands_module.GetRoomTile())
