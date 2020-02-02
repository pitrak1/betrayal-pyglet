import pyglet
from pyglet.gl import *
from src.world import world
from src.commands import add_room_command, add_character_command, key_press_command
from src import camera, assets

game_window = pyglet.window.Window(800, 600)
game_world = world.World()
game_camera = camera.Camera()

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDepthFunc(GL_LEQUAL)

game_window.push_handlers(game_camera)

images = assets.load_images()

command_queue = []
command_queue.append(add_room_command.AddRoomCommand(images['rooms'][0], 3, 3))
command_queue.append(add_room_command.AddRoomCommand(images['rooms'][1], 3, 4))
command_queue.append(add_character_command.AddCharacterCommand(images['brandon_jaspers'], 3, 3))

@game_window.event
def on_draw():
    game_window.clear()
    game_camera.apply()
    game_world.on_draw()

@game_window.event
def on_key_press(symbol, modifiers):
    command_queue.append(key_press_command.KeyPressCommand(symbol, modifiers))

@game_window.event
def on_update(dt):
    while command_queue:
        game_world.on_command(command_queue[0], command_queue)
        del command_queue[0]

    game_world.on_update(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()
