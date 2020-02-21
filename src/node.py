from src.states import commands

class Node():
	def on_draw(self, state):
		raise NotImplementedError('on_draw must be overridden')

	def on_command(self, command, state):	
		if isinstance(command, commands.MousePressCommand):
			return self.mouse_press_handler(command, state)
		elif isinstance(command, commands.KeyPressCommand):
			return self.key_press_handler(command, state)
		elif isinstance(command, commands.AddRoomCommand):
			return self.add_room_handler(command, state)
		elif isinstance(command, commands.AddCharacterCommand):
			return self.add_character_handler(command, state)
		elif isinstance(command, commands.MoveCharacterCommand):
			return self.move_character_handler(command, state)

	def mouse_press_handler(self, command, state):
		self.default_handler(command, state)

	def key_press_handler(self, command, state):
		self.default_handler(command, state)

	def add_room_handler(self, command, state):
		self.default_handler(command, state)

	def add_character_handler(self, command, state):
		self.default_handler(command, state)

	def move_character_handler(self, command, state):
		self.default_handler(command, state)

	def default_handler(self, command, state):
		raise NotImplementedError('default_handler must be overridden')

	def on_update(self, dt, state):
		raise NotImplementedError('on_update must be overridden')
