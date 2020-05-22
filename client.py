import pyglet
from lattice2d.config import Config
from src.client.client_core import ClientCore

CONFIG = {
	'command_types': [
		'client_select',
		'client_adjust_grid',
		'network_start_game',
		'network_get_player_order',
		'network_confirm_player_order',
		'network_get_available_characters',
		'network_get_current_player',
		'network_select_character',
		'network_all_characters_selected',
		'network_get_character_selections',
		'network_confirm_character_selections',
		'network_get_player_positions'
	],
	'log_level': 3,
	'ip_address': '0.0.0.0',
	'port': 8080,
	'full_solution': {
		'network': True,
		'group_count': 6,
		'minimum_players': 1
	}
}

Config(CONFIG)

window = pyglet.window.Window(1280, 720)

@window.event
def on_draw():
	window.clear()
	game.on_draw()

@window.event
def on_update(dt):
	game.on_update(dt)

game = ClientCore()
window.push_handlers(game)
pyglet.clock.schedule_interval(on_update, 1 / 120.0)
pyglet.app.run()
