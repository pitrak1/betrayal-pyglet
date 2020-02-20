from src.utils import position as position_module

GRID_SIZE = 512
DOOR_OFFSET = 18

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def reverse_direction(direction):
	return (direction + 2) % 4

class GridPosition(position_module.Position):
	def __init__(self, grid_x, grid_y):
		self.set_grid_position(grid_x, grid_y)

	def __eq__(self, obj):
		return isinstance(obj, GridPosition) and obj.grid_x == self.grid_x and obj.grid_y == self.grid_y

	def set_grid_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.x = self.grid_x * GRID_SIZE
		self.y = self.grid_y * GRID_SIZE

	def grid_distance(self, grid_position):
		return abs(self.grid_x - grid_position.grid_x) + abs(self.grid_y - grid_position.grid_y)

	def grid_direction(self, grid_position):
		if self.grid_distance(grid_position) > 1:
			raise Exception('direction cannot be computed for distances greater than 1')

		if self == grid_position:
			raise Exception('direction cannot be computed to self')

		if self.grid_x == grid_position.grid_x:
			return DOWN if self.grid_y > grid_position.grid_y else UP
		else:
			return LEFT if self.grid_x > grid_position.grid_x else RIGHT


	def get_door_position(self, direction):
		if direction == UP:
			return position_module.Position(self.x, self.y + (GRID_SIZE // 2 - DOOR_OFFSET))
		elif direction == RIGHT:
			return position_module.Position(self.x + (GRID_SIZE // 2 - DOOR_OFFSET), self.y)
		elif direction == DOWN:
			return position_module.Position(self.x, self.y - (GRID_SIZE // 2 - DOOR_OFFSET))
		else:
			return position_module.Position(self.x - (GRID_SIZE // 2 - DOOR_OFFSET), self.y)

	def up(self):
		return GridPosition(self.grid_x, self.grid_y + 1)

	def right(self):
		return GridPosition(self.grid_x + 1, self.grid_y)

	def down(self):
		return GridPosition(self.grid_x, self.grid_y - 1)

	def left(self):
		return GridPosition(self.grid_x - 1, self.grid_y)

	def copy(self):
		return GridPosition(self.grid_x, self.grid_y)
