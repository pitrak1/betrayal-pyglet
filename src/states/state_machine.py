from src.commands import commands

class StateMachine():
	def __init__(self, queue, room_stack, character_stack):
		self.command_queue = queue
		self.room_stack = room_stack
		self.character_stack = character_stack
		self.current_state = NoSelectionState()

	def is_selected(self, node):
		return self.current_state.__class__.__name__ == 'SelectedState' and self.current_state.selected == node

	def rotate_room(self, grid_x, grid_y, direction):
		self.command_queue.append(commands.AddRoomCommand(self.room_stack.draw(), grid_x, grid_y, 0))
		self.current_state = RotatingRoomState(grid_x, grid_y, direction)

	def is_rotating(self, grid_x, grid_y):
		return self.current_state.__class__.__name__ == 'RotatingRoomState' and self.current_state.grid_x == grid_x and self.current_state.grid_y == grid_y

	def place_room(self):
		self.current_state = NoSelectionState()

	def select(self, selected):
		self.current_state = SelectedState(selected)

	def move(self, grid_x, grid_y, character=None):
		if not character: character = self.current_state.selected
		self.command_queue.append(commands.MoveCharacterCommand(character, grid_x, grid_y))

class NoSelectionState():
	pass

class SelectedState():
	def __init__(self, selected):
		self.selected = selected

class RotatingRoomState():
	def __init__(self, grid_x, grid_y, direction):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.direction = direction
