import math

class Position():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, obj):
		return isinstance(obj, Position) and obj.x == self.x and obj.y == self.y

	def set_position(self, x, y):
		self.x = x
		self.y = y

	def within_circle_bounds(self, position, radius):
		distance = math.sqrt(((self.x - position.x) ** 2) + ((self.y - position.y) ** 2 ))
		return distance < radius // 2

	def within_square_bounds(self, position, width):
		valid_x = position.x > self.x - width // 2 and position.x < self.x + width // 2
		valid_y = position.y > self.y - width // 2 and position.y < self.y + width // 2
		return valid_x and valid_y