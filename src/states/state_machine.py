from src.states import no_selection_state as no_selection_state_module

class StateMachine():
	def __init__(self, queue):
		self.command_queue = queue
		self.current_state = no_selection_state_module.NoSelectionState(self)
