import pyglet
from src.shared import node as node_module

class Label(pyglet.text.Label, node_module.Node):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setup_callbacks()
