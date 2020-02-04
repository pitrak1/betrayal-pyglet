import pytest
import pyglet
from pyglet import sprite
from src.world import room_node
from src.commands import add_character_command

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
    