import pytest
import pyglet
from pyglet import sprite
from src.world import room_node
from src.commands import add_character_command, mouse_press_command, highlight_command

class TestRoomNode():
	class TestConstructor():
		def test_creates_sprite_and_highlighted_sprite(self, mocker, make_room_node):
			make_room_node(mocker)
			sprite.Sprite.assert_called_with('image', 0, 0)
			assert sprite.Sprite.call_count == 2

		def test_adjusts_position_based_on_room_size(self, mocker, make_room_node):
			make_room_node(mocker, grid_x=1, grid_y=2)
			sprite.Sprite.assert_called_with('image', 1 * room_node.ROOM_SIZE, 2 * room_node.ROOM_SIZE)

	class TestOnDraw():
		def test_draws_sprite(self, mocker, make_room_node):
			node = make_room_node(mocker)
			node.on_draw()
			node.sprite.draw.assert_called_once()

		def test_draws_characters(self, mocker, make_room_node_with_stubbed_characters):
			node = make_room_node_with_stubbed_characters(mocker)
			node.on_draw()
			node.characters[0].on_draw.assert_called_once()
			node.characters[1].on_draw.assert_called_once()


	class TestOnCommand():
		class TestWithAddCharacterCommand():
			class TestWhenGridPositionMatches():
				def test_adds_character(self, mocker, make_room_node):
					node = make_room_node(mocker, grid_x=1, grid_y=2)
					command = add_character_command.AddCharacterCommand(img='img', img_highlighted='img', grid_x=1, grid_y=2)
					node.on_command(command, [command])
					assert len(node.characters) == 1

				def test_does_not_pass_to_characters(self, mocker, make_room_node_with_stubbed_characters):
					node = make_room_node_with_stubbed_characters(mocker, grid_x=1, grid_y=2)
					command = add_character_command.AddCharacterCommand(img='img', img_highlighted='img', grid_x=1, grid_y=2)
					node.on_command(command, [command])
					node.characters[0].on_command.assert_not_called()
					node.characters[1].on_command.assert_not_called()

			class TestWhenGridPositionDoesNotMatch():
				def test_does_not_add_character(self, mocker, make_room_node):
					node = make_room_node(mocker, grid_x=1, grid_y=2)
					command = add_character_command.AddCharacterCommand(img='img', img_highlighted='img', grid_x=2, grid_y=2)
					node.on_command(command, [command])
					assert len(node.characters) == 0

				def test_passes_to_characters(self, mocker, make_room_node_with_stubbed_characters):
					node = make_room_node_with_stubbed_characters(mocker, grid_x=1, grid_y=2)
					command = add_character_command.AddCharacterCommand(img='img', img_highlighted='img', grid_x=2, grid_y=2)
					node.on_command(command, [command])
					node.characters[0].on_command.assert_called_once_with(command, [command])
					node.characters[1].on_command.assert_called_once_with(command, [command])
		class TestWithMousePressCommand():
			class TestWhenWithinBounds():
				def test_appends_highlight_command_if_characters_return_false(self, mocker, make_list, make_room_node_with_stubbed_characters):
					node = make_room_node_with_stubbed_characters(mocker)
					command = mouse_press_command.MousePressCommand(x=0, y=0, button='button', modifiers='modifiers')
					node.characters[0].on_command.return_value = False
					node.characters[1].on_command.return_value = False
					queue = make_list(mocker)
					node.on_command(command, queue)
					assert queue.append.call_args[0][0].node == node

				def test_does_not_append_highlight_command_if_a_character_returns_true(self, mocker, make_list, make_room_node_with_stubbed_characters):
					node = make_room_node_with_stubbed_characters(mocker)
					command = mouse_press_command.MousePressCommand(x=0, y=0, button='button', modifiers='modifiers')
					node.characters[0].on_command.return_value = True
					node.characters[1].on_command.return_value = False
					queue = make_list(mocker)
					node.on_command(command, queue)
					queue.append.assert_not_called()
			class TestWhenNotWithinBounds():
				def test_passes_to_characters(self, mocker, make_room_node_with_stubbed_characters):
					node = make_room_node_with_stubbed_characters(mocker)
					command = mouse_press_command.MousePressCommand(x=(room_node.ROOM_SIZE + 10) // 2, y=0, button='button', modifiers='modifiers')
					node.on_command(command, [command])
					node.characters[0].on_command.assert_called_once_with(command, [command])
					node.characters[1].on_command.assert_called_once_with(command, [command])

		class TestWithHighlightCommand():
			def test_sets_highlighted_if_given_self(self, mocker, make_room_node_with_stubbed_characters):
				node = make_room_node_with_stubbed_characters(mocker)
				command = highlight_command.HighlightCommand(node)
				node.on_command(command, [command])
				assert node.highlighted == True

			def test_resets_highlighted_if_not_given_self(self, mocker, make_room_node_with_stubbed_characters):
				node = make_room_node_with_stubbed_characters(mocker)
				other_node = make_room_node_with_stubbed_characters(mocker)
				command = highlight_command.HighlightCommand(other_node)
				node.on_command(command, [command])
				assert node.highlighted == False

			def test_passes_to_characters(self, mocker, make_room_node_with_stubbed_characters):
				node = make_room_node_with_stubbed_characters(mocker)
				command = highlight_command.HighlightCommand(node)
				node.on_command(command, [command])
				node.characters[0].on_command.assert_called_once_with(command, [command])
				node.characters[1].on_command.assert_called_once_with(command, [command])

		class TestWithOtherCommand():
			def test_passes_to_characters(self, mocker, make_room_node_with_stubbed_characters):
				node = make_room_node_with_stubbed_characters(mocker)
				node.on_command('some command', ['some command'])
				node.characters[0].on_command.assert_called_once_with('some command', ['some command'])
				node.characters[1].on_command.assert_called_once_with('some command', ['some command'])

	class TestOnUpdate():
		def test_calls_on_update_for_characters(self, mocker, make_room_node_with_stubbed_characters):
			node = make_room_node_with_stubbed_characters(mocker)
			node.on_update(1)
			node.characters[0].on_update.assert_called_once_with(1)
			node.characters[1].on_update.assert_called_once_with(1)
    