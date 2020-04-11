class AttributeSet():
	def __init__(self, speed, speed_index, might, might_index, sanity, sanity_index, knowledge, knowledge_index):
		self.speed = speed
		self.speed_index = speed_index
		self.might = might
		self.might_index = might_index
		self.sanity = sanity
		self.sanity_index = sanity_index
		self.knowledge = knowledge
		self.knowledge_index = knowledge_index

	def get_attribute_value(self, attribute):
		return getattr(self, attribute)[getattr(self, f'{attribute}_index')]

	def change_attribute_value(self, attribute, change):
		setattr(self, f'{attribute}_index', getattr(self, f'{attribute}_index') + change)

		if getattr(self, f'{attribute}_index') < 0: setattr(self, f'{attribute}_index', 0)
		if getattr(self, f'{attribute}_index') > 8: setattr(self, f'{attribute}_index', 8)

	def is_dead(self):
		return self.speed_index == 0 or self.might_index == 0 or self.sanity_index == 0 or self.knowledge_index == 0