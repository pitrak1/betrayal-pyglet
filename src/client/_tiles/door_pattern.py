ONE_DOOR = 0
RIGHT_ANGLE = 1
ACROSS = 2
ONE_WALL = 3
NO_WALLS = 4

class DoorPattern(list):
	def __init__(self, arg):
		if isinstance(arg, list):
			super().__init__(arg)
			self.__set_code()
		else:
			self.code = arg
			if arg == ONE_DOOR:
				self.extend([True, False, False, False])
			elif arg == RIGHT_ANGLE:
				self.extend([True, True, False, False])
			elif arg == ACROSS:
				self.extend([True, False, True, False])
			elif arg == ONE_WALL:
				self.extend([True, True, True, False])
			else:
				self.extend([True, True, True, True])

	def __set_code(self):
		door_count = self.count(True)

		if door_count == 1:
			self.code = ONE_DOOR
		elif door_count == 2:
			if self[0] != self[1] and self[1] != self[2]:
				self.code = ACROSS
			else:
				self.code = RIGHT_ANGLE
		else:
			self.code = door_count

	def rotate(self, rotation):
		for i in range(rotation):
			self.append(self.pop(0))

	def get_required_doors_in_common(self, obj):
		doors_count = obj.count(True)

		if self.code == ONE_DOOR:
			return 1
		elif self.code == RIGHT_ANGLE:
			if obj.code == ONE_DOOR or obj.code == ACROSS:
				return 1
			else:
				return 2
		elif self.code == ACROSS:
			if obj.code == ONE_DOOR or obj.code == RIGHT_ANGLE:
				return 1
			else:
				return 2
		elif self.code == ONE_WALL:
			return min([3, doors_count])
		else:
			return doors_count

	def get_doors_in_common(self, obj):
		count = 0
		for i in range(4):
			if self[i] and self[i] == obj[i]: count += 1
		return count
