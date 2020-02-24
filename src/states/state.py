from src.states import commands as commands_module

class State():
	def __init__(self, state_machine):
		self.waiting = []
		self.state_machine = state_machine

	def name(self, name):
		if isinstance(name, list):
			return any([x for x in name if x == self.__class__.__name__])
		else:
			return name == self.__class__.__name__

	# Camera

	def trigger_translated_mouse_press(self, x, y, button, modifiers):
		self.state_machine.command_queue.append(commands_module.TranslatedMousePress(x, y, button, modifiers))

	# Tile Stacks

	def set_character_tile(self, tile):
		self.character_tile = tile
		self.check_waiting('set_character_tile')

	def set_room_tile(self, tile):
		self.room_tile = tile
		self.check_waiting('set_room_tile')

	# Asset Manager

	def set_character_asset(self, asset):
		self.character_asset = asset
		self.check_waiting('set_character_asset')

	def set_room_asset(self, asset):
		self.room_asset = asset
		self.check_waiting('set_room_asset')

	def set_misc_asset(self, asset):
		self.misc_asset = asset
		self.check_waiting('set_misc_asset')

	def check_waiting(self, key):
		if self.waiting and key in self.waiting:
			self.waiting = [value for value in self.waiting if value != key]
			if not self.waiting:
				self.waiting_action()
