WINDOW_DIMENSIONS = (1280, 720)

WINDOW_CENTER = (640, 360)

CAMERA_PAN_COEFF = 128
CAMERA_STARTING_ZOOM_FACTOR = 1.0
CAMERA_MAX_ZOOM_FACTOR = 15.0
CAMERA_MIN_ZOOM_FACTOR = 1.0
CAMERA_ZOOM_COEFF = 0.1

GRID_SIZE = 512
DOOR_OFFSET = 18

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

GRID_DIMENSIONS = (20, 20)

CHARACTER_SIZE = 150
AREA_TILE_SIZE = 16

GAME_LIST_PAGE_SIZE = 8

PLAYERS_PER_GAME = 6

BACKGROUND_GROUP = 0
ROOMS_GROUP = 1
CHARACTERS_AND_DOORS_GROUP = 2
HIGHLIGHTS_GROUP = 3

NUMBER_OF_GROUPS = 4

MINIMUM_PLAYERS = 1

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
		'asset_index': 2,
		'doors': [True, True, False, True],
		'floor': 1,
		'grid_position': (0, 0),
		'sprite_rotation': 1
	},
	{
		'display_name': 'Foyer',
		'variable_name': 'foyer',
		'asset_index': 1,
		'doors': [True, True, True, True],
		'floor': 1,
		'grid_position': (0, 1),
		'sprite_rotation': 1
	},
	{
		'display_name': 'Grand Staircase',
		'variable_name': 'grand_staircase',
		'asset_index': 0,
		'doors': [False, False, True, False],
		'floor': 1,
		'grid_position': (0, 2),
		'sprite_rotation': 1
	}
]

ROOMS = [
	{
		'display_name': 'Dungeon',
		'variable_name': 'dungeon',
		'asset_index': 8,
		'doors': [True, False, True, False]
	},
	{
		'display_name': 'Furnace Room',
		'variable_name': 'furnace_room',
		'asset_index': 9,
		'doors': [True, False, True, True]
	},
	{
		'display_name': 'Larder',
		'variable_name': 'larder',
		'asset_index': 10,
		'doors': [True, False, True, False]
	},
	{
		'display_name': 'Pentagram Chamber',
		'variable_name': 'pentagram_chamber',
		'asset_index': 11,
		'doors': [False, True, False, False]
	},
	{
		'display_name': 'Stairs From Basement',
		'variable_name': 'stairs_from_basement',
		'asset_index': 12,
		'doors': [True, False, True, False]
	},
	{
		'display_name': 'Storm Cellar',
		'variable_name': 'storm_cellar',
		'asset_index': 13,
		'doors': [False, True, True, False]
	},
	{
		'display_name': 'Underground Lake',
		'variable_name': 'underground_lake',
		'asset_index': 14,
		'doors': [True, True, False, False]
	},
	{
		'display_name': 'Wine Cellar',
		'variable_name': 'wine_cellar',
		'asset_index': 15,
		'doors': [True, False, True, False]
	},
	{
		'display_name': 'Arsenal',
		'variable_name': 'arsenal',
		'asset_index': 16,
		'doors': [False, True, True, False]
	},
	{
		'display_name': 'Kitchen',
		'variable_name': 'kitchen',
		'asset_index': 17,
		'doors': [True, True, False, False]
	},
	{
		'display_name': 'Laundry',
		'variable_name': 'laundry',
		'asset_index': 18,
		'doors': [False, False, True, True]
	},
	{
		'display_name': 'Menagerie',
		'variable_name': 'menagerie',
		'asset_index': 19,
		'doors': [False, True, False, True]
	},
	{
		'display_name': 'Catacombs',
		'variable_name': 'catacombs',
		'asset_index': 20,
		'doors': [True, False, True, False]
	},
	{
		'display_name': 'Cave',
		'variable_name': 'cave',
		'asset_index': 21,
		'doors': [True, True, True, True]
	},
	{
		'display_name': 'Chasm',
		'variable_name': 'chasm',
		'asset_index': 22,
		'doors': [False, True, False, True]
	},
	{
		'display_name': 'Crypt',
		'variable_name': 'crypt',
		'asset_index': 23,
		'doors': [True, False, False, False]
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