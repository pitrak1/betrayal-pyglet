import pyglet
from src.client import game as game_module
from src.common import constants

window = pyglet.window.Window(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)

@window.event
def on_draw():
	window.clear()
	game.draw()

@window.event
def on_update(dt):
	game.on_update(dt)

game = game_module.Game()
window.push_handlers(game)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()