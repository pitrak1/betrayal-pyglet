from pyglet import sprite

class AbsoluteNode():
	def __init__(self, img, batch, x=0, y=0):
		self.sprite = sprite.Sprite(img, x, y, batch = batch)
		self.children = []
		self.parent = None

	def on_command(self, command, queue):
		for child in self.children:
			child.on_command(command, queue)

	def on_update(self, dt):
		for child in self.children:
			child.on_update(dt)

	def set_transform(self, x, y, rotation, scale_x, scale_y):
		self.sprite.update(x = x, y = y, rotation = rotation, scale_x = scale_x, scale_y = scale_y)

	def add_child(self, child):
		self.children.append(child)
		child.parent = self

	
