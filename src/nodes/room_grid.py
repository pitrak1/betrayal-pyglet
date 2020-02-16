from src.nodes import grid_node, room_node
from src.utils import grid_position

GRID_WIDTH = 20
GRID_HEIGHT = 20

class RoomGrid(list):
	def __init__(self, world, state_machine):
		super().__init__()
		self.world = world
		self.state_machine = state_machine
		for i in range(GRID_WIDTH):
			row = []
			for j in range(GRID_HEIGHT):
				row.append(grid_node.GridNode(state_machine, grid_position.GridPosition(i, j), world))
			self.append(row)

	def get(self, grid_position):
		return self[grid_position.grid_x][grid_position.grid_y]

	def is_room(self, grid_position):
		return isinstance(self.get(grid_position), room_node.RoomNode)

	def get_doors(self, grid_position):
		if not self.is_room(grid_position): raise Exception('cannot read doors without a room')
		return self[grid_position.grid_x][grid_position.grid_y].tile.doors

	def on_draw(self):
		for row in self:
			for room in row:
				if isinstance(room, room_node.RoomNode):
					room.on_draw()

	def add_room(self, command):
		self[command.grid_position.grid_x][command.grid_position.grid_y] = room_node.RoomNode(self.state_machine, command.room_tile, command.grid_position, self.world)
		self.get_doors(command.grid_position).rotate(command.rotation)

	def default_handler(self, callback):
		for row in self:
			for room in row:
				callback(room)

	def on_update(self, callback):
		for row in self:
			for room in row:
				if isinstance(room, room_node.RoomNode):
					callback(room)
