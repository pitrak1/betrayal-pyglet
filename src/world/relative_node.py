import pyglet
from src.world import absolute_node

class RelativeNode(absolute_node.AbsoluteNode):
	relative_x = 0
	relative_y = 0
	relative_rotation = 0.0
	relative_scale_x = 1.0
	relative_scale_y = 1.0

	def on_command(self, command, queue):
		self.update_transform()
		super().on_command(command, queue)

	def on_update(self, dt):
		self.update_transform()
		super().on_update(dt)

	def update_transform(self):
		self.sprite.update(
			x = self.parent.sprite.x + self.relative_x,
			y = self.parent.sprite.y + self.relative_y,
			rotation = self.parent.sprite.rotation + self.relative_rotation,
			scale_x = self.parent.sprite.scale_x * self.relative_scale_x,
			scale_y = self.parent.sprite.scale_y * self.relative_scale_y,
		)

	def set_relative_transform(self, x = 0, y = 0, rotation = 0.0, scale_x = 1.0, scale_y = 1.0):
		self.relative_x = x
		self.relative_y = y
		self.rotation = rotation
		self.scale_x = scale_x
		self.scale_y = scale_y
		self.update_transform()


		