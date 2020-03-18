from src.shared import command, node

class State(node.Node):
	def __init__(self, data, set_state, add_command):
		super().__init__()
		# self.waiting = []
		# self.waiting_action = None
		self.asset_manager = data['assets']
		self.set_state = set_state
		self.add_command = add_command

	def default_handler(self, command, state=None):
		for element in self.elements:
			element.on_command(command, self)

	def on_update(self, dt=None, state=None):
		for element in self.elements:
			element.on_update(dt, self)

	def draw(self):
		for element in self.elements:
			element.draw()

	def trigger_translated_mouse_press(self, x, y, button, modifiers):
		self.add_command(command.Command(
			'client_translated_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def trigger_translated_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(command.Command(
			'client_translated_mouse_drag', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }
		))

	# def check_waiting(self, key):
	# 	if self.waiting and key in self.waiting:
	# 		self.waiting = [value for value in self.waiting if value != key]
	# 		if not self.waiting:
	# 			self.waiting_action()
