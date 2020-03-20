import random
import threading
from src.server.states import lobby_state
from src.shared import threaded_queue, stringify, threaded_sync, node
import config

class Game(node.Node):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.players = []
		self.rooms = []
		self.command_queue = threaded_queue.ThreadedQueue()
		data = { 'players': self.players, 'rooms': self.rooms, 'name': name }
		self.current_state = lobby_state.LobbyState(data, self.set_state, self.command_queue.append)

	def set_state(self, state):
		self.current_state = state

	def add_command(self, command):
		self.command_queue.append(command)

	def on_update(self, dt=None, state=None):
		while self.command_queue.has_elements():
			command = self.command_queue.pop_front()
			self.current_state.on_command(command)
