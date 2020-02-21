import pyglet
from pyglet.gl import *
from src.nodes import world_node, room_node
from src.states import state_machine, commands
from src.tiles import room_tile_stack, character_tile_stack
from src.assets import asset_manager as asset_manager_module
from src.camera import camera
from src.utils import grid_position, constants

game_window = pyglet.window.Window(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
asset_manager = asset_manager_module.AssetManager()
images = asset_manager.images
room_stack = room_tile_stack.RoomTileStack(images)
character_stack = character_tile_stack.CharacterTileStack(images)

command_queue = []
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Entrance Hall'), grid_position.GridPosition(10, 10), 1))
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Foyer'), grid_position.GridPosition(10, 11), 0))
command_queue.append(commands.AddRoomCommand(room_stack.get_by_name('Grand Staircase'), grid_position.GridPosition(10, 12), 2))
command_queue.append(commands.AddCharacterCommand(character_stack.get_by_name('Brandon Jaspers'), grid_position.GridPosition(10, 10)))

game_state_machine = state_machine.StateMachine(command_queue, room_stack, character_stack)
game_world_node = world_node.WorldNode()
game_camera = camera.Camera()

@game_window.event
def on_draw():
    game_window.clear()
    game_camera.on_draw(game_state_machine.current_state)
    game_world_node.on_draw(game_state_machine.current_state)

@game_window.event
def on_key_press(symbol, modifiers):
    command_queue.append(commands.KeyPressCommand(symbol, modifiers))

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    command_queue.append(commands.RawMousePressCommand(x, y, button, modifiers))

@game_window.event
def on_mouse_scroll(x, y, dx, dy):
    command_queue.append(commands.MouseScrollCommand(x, y, dx, dy))

@game_window.event
def on_update(dt):
    while command_queue:
        command = command_queue.pop(0)
        game_world_node.on_command(command, game_state_machine.current_state)
        game_camera.on_command(command, game_state_machine.current_state)

    game_world_node.on_update(dt, game_state_machine.current_state)
    game_camera.on_update(dt, game_state_machine.current_state, key_handler)

key_handler = pyglet.window.key.KeyStateHandler()
game_window.push_handlers(key_handler)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(on_update, 1 / 120.0)
    pyglet.app.run()
