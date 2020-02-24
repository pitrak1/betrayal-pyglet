from src.states import state as state_module, selected_state as selected_state_module, commands as commands_module

class NoSelectionState(state_module.State):
	def select(self, selected):
		self.state_machine.current_state = selected_state_module.SelectedState(self.state_machine, selected)
		self.state_machine.command_queue.append(commands_module.Select(selected))
