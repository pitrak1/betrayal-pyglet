import pyglet
from pyglet.gl import *
from src.world import world_node
from src.state import state_machine
from src.commands import commands
from src import camera, assets

game_window = pyglet.window.Window(800, 600)
images = assets.load_images()
command_queue = []
command_queue.append(commands.AddRoomCommand(images['rooms'][0], images['rooms_selected'][0], 0, 0))
command_queue.append(commands.AddRoomCommand(images['rooms'][1], images['rooms_selected'][1], 0, 1))
command_queue.append(commands.AddCharacterCommand(images['brandon_jaspers'], images['brandon_jaspers_selected'], 0, 1))

game_state_machine = state_machine.StateMachine(command_queue)
game_world_node = world_node.WorldNode(game_state_machine)


keys = pyglet.window.key.KeyStateHandler()
game_window.push_handlers(keys)
game_camera = camera.Camera(keys)
game_window.push_handlers(game_camera)


@game_window.event
def on_draw():
    game_window.clear()
    game_camera.apply()
    game_world_node.on_draw()

@game_window.event
def on_key_press(symbol, modifiers):
    command_queue.append(commands.KeyPressCommand(symbol, modifiers))

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    coordinates = game_camera.translate_window_to_absolute_coordinates(x, y)
    command_queue.append(commands.MousePressCommand(coordinates[0], coordinates[1], button, modifiers))

@game_window.event
def on_update(dt):
    while command_queue:
        game_world_node.on_command(command_queue[0])
        del command_queue[0]

    game_world_node.on_update(dt)
    game_camera.on_update(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()
