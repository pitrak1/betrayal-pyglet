from src.shared import node as node_module

class ServerCharacter(node_module.Node):
	def __init__(self, entry):
		super().__init__()
		self.entry = entry
		for key, value in entry.items():
			setattr(self, key, value)

	def get_attribute_value(self, attribute):
		return getattr(self, attribute)[getattr(self, f'{attribute}_index')]

	def change_attribute_value(self, attribute, change):
		setattr(self, f'{attribute}_index', getattr(self, f'{attribute}_index') + change)

		if getattr(self, f'{attribute}_index') < 0: setattr(self, f'{attribute}_index', 0)
		if getattr(self, f'{attribute}_index') > 8: setattr(self, f'{attribute}_index', 8)

	def is_dead(self):
		return self.speed_index == 0 or self.might_index == 0 or self.sanity_index == 0 or self.knowledge_index == 0