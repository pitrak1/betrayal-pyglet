from src.utils import constants

def get_distance(start_x, start_y, end_x, end_y):
	return abs(start_x - end_x) + abs(start_y - end_y)

def get_direction(start_x, start_y, end_x, end_y):
	distance = get_distance(start_x, start_y, end_x, end_y)
	if distance > 1:
		raise Exception('direction cannot be computed for distances greater than 1')

	if distance == 0 :
		raise Exception('direction cannot be computed to self')

	if start_x == end_x:
		return constants.DOWN if start_y > end_y else constants.UP
	else:
		return constants.LEFT if start_x > end_x else constants.RIGHT

def get_door_position(grid_x, grid_y, direction):
	offset = (constants.GRID_SIZE // 2 - constants.DOOR_OFFSET)
	if direction == constants.UP:
		return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE + offset }
	elif direction == constants.RIGHT:
		return { 'x': grid_x * constants.GRID_SIZE + offset, 'y': grid_y * constants.GRID_SIZE }
	elif direction == constants.DOWN:
		return { 'x': grid_x * constants.GRID_SIZE, 'y': grid_y * constants.GRID_SIZE - offset }
	else:
		return { 'x': grid_x * constants.GRID_SIZE - offset, 'y': grid_y * constants.GRID_SIZE }
