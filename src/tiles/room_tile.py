from pyglet import sprite, text
from src.tiles import tile

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DOOR_OFFSET = 18

PATTERN_ONE_DOOR = 0
PATTERN_RIGHT_ANGLE = 1
PATTERN_ACROSS = 2
PATTERN_ONE_WALL = 3
PATTERN_NO_WALLS = 4

PATTERNS = [
	[True, False, False, False],
	[True, True, False, False],
	[True, False, True, False],
	[True, True, True, False],
	[True, True, True, True]
]

def find_pattern(pattern):
	count = pattern.count(True)

	if count == 1:
		return PATTERN_ONE_DOOR
	elif count == 2:
		if pattern[0] != pattern[1] and pattern[1] != pattern[2]:
			return PATTERN_ACROSS
		else:
			return PATTERN_RIGHT_ANGLE
	elif count == 3:
		return PATTERN_ONE_WALL
	else:
		return PATTERN_NO_WALLS

class RoomTile(tile.Tile):
	def __init__(self, name, images, room_number, pattern):
		super().__init__(name, images['rooms'][room_number], images['room_selected'])
		self.pattern = pattern
		self.door_presence = PATTERNS[pattern].copy()
		self.doors = [
			sprite.Sprite(images['door']),
			sprite.Sprite(images['door']), 
			sprite.Sprite(images['door']), 
			sprite.Sprite(images['door'])
		]

	def set_position(self, grid_x, grid_y):
		super().set_position(grid_x, grid_y)
		x = grid_x * tile.GRID_SIZE
		y = grid_y * tile.GRID_SIZE

		self.doors[0].update(x=x, y=y + (tile.GRID_SIZE // 2) - DOOR_OFFSET)
		self.doors[1].update(x=x + (tile.GRID_SIZE // 2) - DOOR_OFFSET, y=y, rotation=90)
		self.doors[2].update(x=x, y=y - (tile.GRID_SIZE // 2) + DOOR_OFFSET, rotation=180)
		self.doors[3].update(x=x - (tile.GRID_SIZE // 2) + DOOR_OFFSET, y=y, rotation=270)

	def rotate(self, rotation):
		for i in range(rotation):
			self.door_presence.append(self.door_presence.pop(0))

	def on_draw(self, is_selected):
		super().on_draw(is_selected)

		for i in range(4):
			if self.door_presence[i]: self.doors[i].draw()

	def within_bounds(self, x, y):
		valid_x = x > self.sprite.x - tile.GRID_SIZE // 2 and x < self.sprite.x + tile.GRID_SIZE // 2
		valid_y = y > self.sprite.y - tile.GRID_SIZE // 2 and y < self.sprite.y + tile.GRID_SIZE // 2
		return valid_x and valid_y
