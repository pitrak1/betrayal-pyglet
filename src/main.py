import pyglet
from pyglet.gl import *
from world import world
import camera

game_window = pyglet.window.Window(800, 600)
game_world = world.World()
game_camera = camera.Camera()

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDepthFunc(GL_LEQUAL)

game_window.on_mouse_drag = game_camera.on_mouse_drag
game_window.on_mouse_scroll = game_camera.on_mouse_scroll

@game_window.event
def on_draw():
    game_window.clear()
    game_camera.apply()
    game_world.draw()

# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == pyglet.window.mouse.LEFT:
#         print('The left mouse button was pressed.')

# @window.event
# def update(dt):
#     print('update')

if __name__ == "__main__":
    # pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
