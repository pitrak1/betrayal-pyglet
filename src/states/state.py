from src.states import commands as commands_module

class State():
	def __init__(self, state_machine):
		self.state_machine = state_machine

	def translate_mouse_press(self, position, button, modifiers):
		self.state_machine.command_queue.append(commands_module.TranslatedMousePressCommand(position, button, modifiers))