import pyglet
from pyglet.gl import *
from src.world import world
from src import camera
from src.commands import *

game_window = pyglet.window.Window(800, 600)
game_world = world.World()
game_camera = camera.Camera()

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDepthFunc(GL_LEQUAL)

game_window.push_handlers(game_camera)

event_stack = []

@game_window.event
def on_draw():
    game_window.clear()
    game_camera.apply()
    game_world.draw()

@game_window.event
def on_key_press(symbol, modifiers):
    command = src.commands.key_press_command.KeyPressCommand(symbol, modifiers)
    event_stack.append(command)

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == pyglet.window.mouse.LEFT:
#         print('The left mouse button was pressed.')

@game_window.event
def update(dt):
	while event_stack:
		game_world.update(dt, event_stack[0])
		del event_stack[0]

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
