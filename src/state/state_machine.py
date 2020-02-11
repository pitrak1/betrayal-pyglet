from src.commands import commands

class StateMachine():
	def __init__(self, queue):
		self.command_queue = queue
		self.current_state = NoSelectionState()

	def is_selected(self, node):
		return self.current_state.__class__.__name__ == 'SelectedState' and self.current_state.selected == node

	def select(self, selected):
		self.current_state = SelectedState(selected)

class NoSelectionState():
	pass

class SelectedState():
	def __init__(self, selected):
		self.selected = selected
