import pyglet
from src import game as game_module
from src.utils import constants

game_window = pyglet.window.Window(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)

@game_window.event
def on_draw():
    game.on_draw()

@game_window.event
def on_key_press(symbol, modifiers):
    game.on_key_press(symbol, modifiers)

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    game.on_mouse_press(x, y, button, modifiers)

@game_window.event
def on_mouse_scroll(x, y, dx, dy):
    game.on_mouse_scroll(x, y, dx, dy)

@game_window.event
def on_update(dt):
    game.on_update(dt)

game = game_module.Game(game_window)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()
