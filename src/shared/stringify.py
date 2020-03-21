from src.shared import command as command_module

def stringify(command):
	data_string = f'{command.type};'
	for key, value in command.data.items():
		if key == 'connection': continue
		data_string += __stringify_data_item(key, value)
	print(f'stringified {data_string[:-1]}*')
	return f'{data_string[:-1]}*'.encode()

def __stringify_data_item(data_item_key, data_item_value):
	result_string = f'{data_item_key}='
	if isinstance(data_item_value, list):
		result_string += __stringify_list(data_item_value)
	elif isinstance(data_item_value, str):
		result_string += data_item_value
	return f'{result_string};'

def __stringify_list(list_value):
	result_string = '['
	elements = False
	for value in list_value:
		elements = True
		if isinstance(value, tuple):
			result_string += f'{__stringify_tuple(value)}|'
		elif isinstance(value, str):
			result_string += f'{value}|'

	if elements:
		return result_string[:-1] + ']'
	else:
		return '[]'

def __stringify_tuple(tuple_value):
	result_string = ''
	for value in tuple_value:
		result_string += f'{value},'
	return result_string[:-1]


def destringify(received):
	commands = received.decode().split('*')[:-1]
	result = []
	for command_string in commands:
		print(f'destringified {command_string}')
		result.append(__destringify_each(command_string))
	return result

def __destringify_each(command_string):
	values = command_string.split(';')
	result = command_module.Command(values[0], {})
	for data_item in values[1:]:
		key, value = data_item.split('=')
		if __destringify_is_list(value):
			result.data[key] = __destringify_list(value)
		else:
			result.data[key] = value
	return result

def __destringify_is_list(list_value):
	return '[' in list_value

def __destringify_list(list_value):
	list_value = list_value[1:-1]
	values = list_value.split('|')
	result = []
	for value in values:
		if __destringify_is_tuple(value):
			result.append(tuple(value.split(',')))
		else:
			result.append(value)
	return result

def __destringify_is_tuple(tuple_value):
	return len(tuple_value.split(',')) > 1

