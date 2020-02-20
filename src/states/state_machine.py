from src.states import no_selection_state as no_selection_state_module

class StateMachine():
	def __init__(self, queue, room_stack, character_stack):
		self.command_queue = queue
		self.room_stack = room_stack
		self.character_stack = character_stack
		self.current_state = no_selection_state_module.NoSelectionState(self)
