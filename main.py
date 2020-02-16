import pyglet
from pyglet.gl import *
from src.nodes import world_node, room_node
from src.states import state_machine
from src.commands import commands
from src.tiles import room_tile_stack, character_tile_stack
from src import camera, assets
from src.utils import grid_position

game_window = pyglet.window.Window(800, 600)
images = assets.load_images()
room_stack = room_tile_stack.RoomTileStack(images)
character_stack = character_tile_stack.CharacterTileStack(images)

command_queue = []
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Entrance Hall'), grid_position.GridPosition(10, 10), 1))
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Foyer'), grid_position.GridPosition(10, 11), 0))
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Grand Staircase'), grid_position.GridPosition(10, 12), 2))
command_queue.append(commands.AddCharacterCommand(character_stack.get_by_name('Brandon Jaspers'), grid_position.GridPosition(10, 10)))

game_state_machine = state_machine.StateMachine(command_queue, room_stack, character_stack)
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
    position = game_camera.translate_window_to_absolute_coordinates(x, y)
    command_queue.append(commands.MousePressCommand(position, button, modifiers))

@game_window.event
def on_update(dt):
    while command_queue:
        game_world_node.on_command(command_queue.pop(0))

    game_world_node.on_update(dt)
    game_camera.on_update(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()
