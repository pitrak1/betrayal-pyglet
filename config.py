INET_ADDRESS = '0.0.0.0'
INET_PORT = 8080

# Recommended that assets are 150 pixels wide and circular
CHARACTERS = [
	{
		'display_name': 'Heather Granville',
		'variable_name': 'heather_granville',
		'portrait_asset': 'heather_granville.png',
		'speed': [0, 3, 3, 4, 5, 6, 6, 7, 8],
		'speed_index': 3,
		'might': [0, 3, 3, 3, 4, 5, 6, 7, 8],
		'might_index': 3,
		'sanity': [0, 3, 3, 3, 4, 5, 6, 6, 6],
		'sanity_index': 3,
		'knowledge': [0, 2, 3, 3, 4, 5, 6, 7, 8],
		'knowledge_index': 5,
		'related': ['jenny_leclerc']
	},
	{
		'display_name': 'Jenny LeClerc',
		'variable_name': 'jenny_leclerc',
		'portrait_asset': 'jenny_leclerc.png',
		'speed': [0, 2, 3, 4, 4, 4, 5, 6, 8],
		'speed_index': 4,
		'might': [0, 3, 4, 4, 4, 4, 5, 6, 8],
		'might_index': 3,
		'sanity': [0, 1, 1, 2, 4, 4, 4, 5, 6],
		'sanity_index': 5,
		'knowledge': [0, 2, 3, 3, 4, 4, 5, 6, 8],
		'knowledge_index': 3,
		'related': ['heather_granville']
	},
	{
		'display_name': 'Madame Zostra',
		'variable_name': 'madame_zostra',
		'portrait_asset': 'madame_zostra.png',
		'speed': [0, 2, 3, 3, 5, 5, 6, 6, 7],
		'speed_index': 3,
		'might': [0, 2, 3, 3, 4, 5, 5, 5, 6],
		'might_index': 4,
		'sanity': [0, 4, 4, 4, 5, 6, 7, 8, 8],
		'sanity_index': 3,
		'knowledge': [0, 1, 3, 4, 4, 4, 5, 6, 6],
		'knowledge_index': 4,
		'related': ['vivian_lopez']
	},
	{
		'display_name': 'Vivian Lopez',
		'variable_name': 'vivian_lopez',
		'portrait_asset': 'vivian_lopez.png',
		'speed': [0, 3, 4, 4, 4, 4, 6, 7, 8],
		'speed_index': 4,
		'might': [0, 2, 2, 2, 4, 4, 5, 6, 6],
		'might_index': 3,
		'sanity': [0, 4, 4, 4, 5, 6, 7, 8, 8],
		'sanity_index': 3,
		'knowledge': [0, 4, 5, 5, 5, 5, 6, 6, 7],
		'knowledge_index': 4,
		'related': ['madame_zostra']
	},
	{
		'display_name': 'Brandon Jaspers',
		'variable_name': 'brandon_jaspers',
		'portrait_asset': 'brandon_jaspers.png',
		'speed': [0, 3, 4, 4, 4, 5, 6, 7, 8],
		'speed_index': 3,
		'might': [0, 2, 3, 3, 4, 5, 6, 6, 7],
		'might_index': 4,
		'sanity': [0, 3, 3, 3, 4, 5, 6, 7, 8],
		'sanity_index': 4,
		'knowledge': [0, 1, 3, 3, 5, 5, 6, 6, 7],
		'knowledge_index': 3,
		'related': ['peter_akimoto']
	},
	{
		'display_name': 'Peter Akimoto',
		'variable_name': 'peter_akimoto',
		'portrait_asset': 'peter_akimoto.png',
		'speed': [0, 3, 3, 3, 4, 6, 6, 7, 7],
		'speed_index': 4,
		'might': [0, 2, 3, 3, 4, 5, 5, 6, 8],
		'might_index': 3,
		'sanity': [0, 3, 4, 4, 4, 5, 6, 6, 7],
		'sanity_index': 4,
		'knowledge': [0, 3, 4, 4, 5, 6, 7, 7, 8],
		'knowledge_index': 3,
		'related': ['brandon_jaspers']
	},
	{
		'display_name': 'Darrin Williams',
		'variable_name': 'darrin_williams',
		'portrait_asset': 'darrin_williams.png',
		'speed': [0, 4, 4, 4, 5, 6, 7, 7, 8],
		'speed_index': 5,
		'might': [0, 2, 3, 3, 4, 5, 6, 6, 7],
		'might_index': 3,
		'sanity': [0, 1, 2, 3, 4, 5, 5, 5, 7],
		'sanity_index': 3,
		'knowledge': [0, 2, 3, 3, 4, 5, 5, 5, 7],
		'knowledge_index': 3,
		'related': ['ox_bellows']
	},
	{
		'display_name': 'Ox Bellows',
		'variable_name': 'ox_bellows',
		'portrait_asset': 'ox_bellows.png',
		'speed': [0, 2, 2, 2, 3, 4, 5, 5, 6],
		'speed_index': 5,
		'might': [0, 4, 5, 5, 6, 6, 7, 8, 8],
		'might_index': 3,
		'sanity': [0, 2, 2, 3, 4, 5, 5, 6, 7],
		'sanity_index': 3,
		'knowledge': [0, 2, 2, 3, 3, 5, 5, 6, 6],
		'knowledge_index': 3,
		'related': ['darrin_williams']
	},
	{
		'display_name': 'Zoe Ingstrom',
		'variable_name': 'zoe_ingstrom',
		'portrait_asset': 'zoe_ingstrom.png',
		'speed': [0, 4, 4, 4, 4, 5, 6, 8, 8],
		'speed_index': 4,
		'might': [0, 2, 2, 3, 3, 4, 4, 6, 7],
		'might_index': 4,
		'sanity': [0, 3, 4, 5, 5, 6, 6, 7, 8],
		'sanity_index': 3,
		'knowledge': [0, 1, 2, 3, 4, 4, 5, 5, 5],
		'knowledge_index': 3,
		'related': ['missy_dubourde']
	},
	{
		'display_name': 'Missy Dubourde',
		'variable_name': 'missy_dubourde',
		'portrait_asset': 'missy_dubourde.png',
		'speed': [0, 3, 4, 5, 6, 6, 6, 7, 7],
		'speed_index': 3,
		'might': [0, 2, 3, 3, 3, 4, 5, 6, 7],
		'might_index': 4,
		'sanity': [0, 1, 2, 3, 4, 5, 5, 6, 7],
		'sanity_index': 3,
		'knowledge': [0, 2, 3, 4, 4, 5, 6, 6, 6],
		'knowledge_index': 4,
		'related': ['zoe_ingstrom']
	},
	{
		'display_name': 'Professor Longfellow',
		'variable_name': 'professor_longfellow',
		'portrait_asset': 'professor_longfellow.png',
		'speed': [0, 2, 2, 4, 4, 5, 5, 6, 6],
		'speed_index': 4,
		'might': [0, 1, 2, 3, 4, 5, 5, 6, 6],
		'might_index': 3,
		'sanity': [0, 1, 3, 3, 4, 5, 5, 6, 7],
		'sanity_index': 3,
		'knowledge': [0, 4, 5, 5, 5, 5, 6, 7, 8],
		'knowledge_index': 5,
		'related': ['father_rhinehardt']
	},
	{
		'display_name': 'Father Rhinehardt',
		'variable_name': 'father_rhinehardt',
		'portrait_asset': 'father_rhinehardt.png',
		'speed': [0, 2, 3, 3, 4, 5, 6, 7, 7],
		'speed_index': 3,
		'might': [0, 1, 2, 2, 4, 4, 5, 5, 7],
		'might_index': 3,
		'sanity': [0, 3, 4, 5, 5, 6, 7, 7, 8],
		'sanity_index': 5,
		'knowledge': [0, 1, 3, 3, 4, 5, 6, 6, 8],
		'knowledge_index': 4,
		'related': ['professor_longfellow']
	}
]

STARTING_ROOMS = [
	{
		'display_name': 'Entrance Hall',
		'variable_name': 'entrance_hall',
		'asset_index': 0,
		'doors': [True, True, False, True],
		'floor': 1,
		'grid_x': 0,
		'grid_y': 0,
		'sprite_rotation': 1
	},
	{
		'display_name': 'Foyer',
		'variable_name': 'foyer',
		'asset_index': 1,
		'doors': [True, True, True, True],
		'floor': 1,
		'grid_x': 0,
		'grid_y': 1,
		'sprite_rotation': 1
	},
	{
		'display_name': 'Grand Staircase',
		'variable_name': 'grand_staircase',
		'asset_index': 2,
		'doors': [False, False, True, False],
		'floor': 1,
		'grid_x': 0,
		'grid_y': 2,
		'sprite_rotation': 1
	}
]

COMMON_ASSETS = {
	'button': { 'asset_type': 'multiple', 'asset': 'brown_button.png', 'rows': 3, 'columns': 3 },
	'area': { 'asset_type': 'multiple', 'asset': 'white_button.png', 'rows': 3, 'columns': 3 },
	'text_box': { 'asset_type': 'multiple', 'asset': 'brown_button.png', 'rows': 3, 'columns': 3 },
	'host_marker': { 'asset_type': 'single', 'asset': 'crown.png' },
	'menu_background': { 'asset_type': 'single', 'asset': 'menu_background.jpg' },
	'door': { 'asset_type': 'single', 'asset': 'door.png' },
	'room_selected': { 'asset_type': 'single', 'asset': 'room_selected.png' },
	'character_selected': { 'asset_type': 'single', 'asset': 'character_selected.png' },
	'attribute_highlight': { 'asset_type': 'single', 'asset': 'attribute_highlight.png' }
}

ROOMS_ASSET = {
	'asset': 'rooms.jpg',
	'rows': 9,
	'columns': 8
}

ONE_DOOR = 0
RIGHT_ANGLE = 1
ACROSS = 2
ONE_WALL = 3
NO_WALLS = 4