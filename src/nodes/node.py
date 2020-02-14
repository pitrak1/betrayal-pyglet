from src.commands import commands

class Node():
	def __init__(self, state_machine):
		self.state_machine = state_machine

	def on_draw(self):
		raise NotImplementedException('on_draw must be overridden')

	def on_command(self, command):	
		if isinstance(command, commands.MousePressCommand):
			return self.mouse_press_handler(command)
		elif isinstance(command, commands.KeyPressCommand):
			return self.key_press_handler(command)
		elif isinstance(command, commands.AddRoomCommand):
			return self.add_room_handler(command)
		elif isinstance(command, commands.AddCharacterCommand):
			return self.add_character_handler(command)
		elif isinstance(command, commands.MoveCharacterCommand):
			return self.move_character_handler(command)

	def mouse_press_handler(self, command):
		self.default_handler(command)

	def key_press_handler(self, command):
		self.default_handler(command)

	def add_room_handler(self, command):
		self.default_handler(command)

	def add_character_handler(self, command):
		self.default_handler(command)

	def move_character_handler(self, command):
		self.default_handler(command)

	def default_handler(self, command):
		raise NotImplementedException('default_handler must be overridden')

	def on_update(self, dt):
		raise NotImplementedException('on_update must be overridden')
