ONE_DOOR = 0
RIGHT_ANGLE = 1
ACROSS = 2
ONE_WALL = 3
NO_WALLS = 4

def get_code(doors):
	door_count = doors.count(True)

	if door_count == 1:
		return ONE_DOOR
	elif door_count == 2:
		if doors[0] != doors[1] and doors[1] != doors[2]:
			return ACROSS
		else:
			return RIGHT_ANGLE
	else:
		return door_count

def rotate(doors, rotation):
	for i in range(rotation):
		doors.append(doors.pop(0))
	return doors

def get_required_doors_in_common(doors, other_doors):
	other_doors_count = other_doors.count(True)
	code = get_code(doors)
	other_code = get_code(other_doors)

	if code == ONE_DOOR:
		return 1
	elif code == RIGHT_ANGLE:
		if other_code == ONE_DOOR or other_code == ACROSS:
			return 1
		else:
			return 2
	elif code == ACROSS:
		if other_code == ONE_DOOR or other_code == RIGHT_ANGLE:
			return 1
		else:
			return 2
	elif code == ONE_WALL:
		return min([3, other_doors_count])
	else:
		return other_doors_count

def get_doors_in_common(doors, other_doors):
	count = 0
	for i in range(4):
		if doors[i] and doors[i] == other_doors[i]: count += 1
	return count
