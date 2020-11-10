class Constants:
	window_dimensions = (1280, 720)
	window_dimensions_x = window_dimensions[0]
	window_dimensions_y = window_dimensions[1]

	window_center = (640, 360)
	window_center_x = window_center[0]
	window_center_y = window_center[1]

	camera_pan_coeff = 128
	camera_starting_zoom_factor = 1.0
	camera_max_zoom_factor = 15.0
	camera_min_zoom_factor = 1.0
	camera_zoom_coeff = 0.1

	grid_dimensions = (10, 10)
	grid_dimensions_x = grid_dimensions[0]
	grid_dimensions_y = grid_dimensions[1]
	grid_size = 512
	character_size = 150
	area_tile_size = 16
	door_offset = 18

	game_list_page_size = 4
	max_players_per_game = 6
	min_players_per_game = 1

	characters = [
		{
			'display_name': 'Heather Granville',
			'key': 'heather_granville',
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
			'key': 'jenny_leclerc',
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
			'key': 'madame_zostra',
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
			'key': 'vivian_lopez',
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
			'key': 'brandon_jaspers',
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
			'key': 'peter_akimoto',
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
			'key': 'darrin_williams',
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
			'key': 'ox_bellows',
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
			'key': 'zoe_ingstrom',
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
			'key': 'missy_dubourde',
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
			'key': 'professor_longfellow',
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
			'key': 'father_rhinehardt',
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

	starting_rooms = [
		{
			'display_name': 'Entrance Hall',
			'key': 'entrance_hall',
			'asset_index': 2,
			'doors': [True, True, False, True],
			'floor': 1,
			'grid_position': (0, 0),
			'sprite_rotation': 1
		},
		{
			'display_name': 'Foyer',
			'key': 'foyer',
			'asset_index': 1,
			'doors': [True, True, True, True],
			'floor': 1,
			'grid_position': (0, 1),
			'sprite_rotation': 1
		},
		{
			'display_name': 'Grand Staircase',
			'key': 'grand_staircase',
			'asset_index': 0,
			'doors': [False, False, True, False],
			'floor': 1,
			'grid_position': (0, 2),
			'sprite_rotation': 1
		}
	]

	rooms = [
		{
			'display_name': 'Dungeon',
			'key': 'dungeon',
			'asset_index': 8,
			'doors': [True, False, True, False]
		},
		{
			'display_name': 'Furnace Room',
			'key': 'furnace_room',
			'asset_index': 9,
			'doors': [True, False, True, True]
		},
		{
			'display_name': 'Larder',
			'key': 'larder',
			'asset_index': 10,
			'doors': [True, False, True, False]
		},
		{
			'display_name': 'Pentagram Chamber',
			'key': 'pentagram_chamber',
			'asset_index': 11,
			'doors': [False, True, False, False]
		},
		{
			'display_name': 'Stairs From Basement',
			'key': 'stairs_from_basement',
			'asset_index': 12,
			'doors': [True, False, True, False]
		},
		{
			'display_name': 'Storm Cellar',
			'key': 'storm_cellar',
			'asset_index': 13,
			'doors': [False, True, True, False]
		},
		{
			'display_name': 'Underground Lake',
			'key': 'underground_lake',
			'asset_index': 14,
			'doors': [True, True, False, False]
		},
		{
			'display_name': 'Wine Cellar',
			'key': 'wine_cellar',
			'asset_index': 15,
			'doors': [True, False, True, False]
		},
		{
			'display_name': 'Arsenal',
			'key': 'arsenal',
			'asset_index': 16,
			'doors': [False, True, True, False]
		},
		{
			'display_name': 'Kitchen',
			'key': 'kitchen',
			'asset_index': 17,
			'doors': [True, True, False, False]
		},
		{
			'display_name': 'Laundry',
			'key': 'laundry',
			'asset_index': 18,
			'doors': [False, False, True, True]
		},
		{
			'display_name': 'Menagerie',
			'key': 'menagerie',
			'asset_index': 19,
			'doors': [False, True, False, True]
		},
		{
			'display_name': 'Catacombs',
			'key': 'catacombs',
			'asset_index': 20,
			'doors': [True, False, True, False]
		},
		{
			'display_name': 'Cave',
			'key': 'cave',
			'asset_index': 21,
			'doors': [True, True, True, True]
		},
		{
			'display_name': 'Chasm',
			'key': 'chasm',
			'asset_index': 22,
			'doors': [False, True, False, True]
		},
		{
			'display_name': 'Crypt',
			'key': 'crypt',
			'asset_index': 23,
			'doors': [True, False, False, False]
		}
	]

	door_layout_one_door = 0
	door_layout_right_angle = 1
	door_layout_across = 2
	door_layout_one_wall = 3
	door_layout_no_walls = 4
