from pyglet import sprite, text
from src import assets

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DOOR_OFFSET = 18

ROOM_SIZE = 512

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

class RoomTile():
	def __init__(self, images, name, room_number, pattern):
		self.sprite = sprite.Sprite(images['rooms'][room_number])
		self.selected = sprite.Sprite(images['room_selected'])
		self.door_presence = PATTERNS[pattern].copy()
		self.doors = [
			sprite.Sprite(images['door']),
			sprite.Sprite(images['door']), 
			sprite.Sprite(images['door']), 
			sprite.Sprite(images['door'])
		]
		self.label = text.Label(name)

	def set_position(self, grid_x, grid_y):
		x = grid_x * ROOM_SIZE
		y = grid_y * ROOM_SIZE

		self.sprite.update(x=x, y=y)
		self.selected.update(x=x, y=y)

		self.label.x = x
		self.label.y = y

		self.doors[0].update(x=x, y=y + (ROOM_SIZE // 2) - DOOR_OFFSET)
		self.doors[1].update(x=x + (ROOM_SIZE // 2) - DOOR_OFFSET, y=y, rotation=90)
		self.doors[2].update(x=x, y=y - (ROOM_SIZE // 2) + DOOR_OFFSET, rotation=180)
		self.doors[3].update(x=x - (ROOM_SIZE // 2) + DOOR_OFFSET, y=y, rotation=270)



	def on_draw(self, is_selected):
		self.sprite.draw()
		if is_selected: self.selected.draw()
		self.label.draw()

		for i in range(4):
			if self.door_presence[i]: self.doors[i].draw()

	def within_bounds(self, x, y):
		valid_x = x > self.sprite.x - ROOM_SIZE // 2 and x < self.sprite.x + ROOM_SIZE // 2
		valid_y = y > self.sprite.y - ROOM_SIZE // 2 and y < self.sprite.y + ROOM_SIZE // 2
		return valid_x and valid_y
