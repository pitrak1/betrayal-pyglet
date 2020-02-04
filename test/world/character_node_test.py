import pytest
import pyglet
from pyglet import sprite
from src.world import character_node

class TestCharacterNode():
	class TestConstructor():
		def test_creates_sprite_and_highlighted_sprite(self, mocker, make_character_node):
			make_character_node(mocker)
			sprite.Sprite.assert_called_with('image', 0, 0)
			assert sprite.Sprite.call_count == 2

	class TestOnDraw():
		def test_draws_sprite(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.on_draw()
			node.sprite.draw.assert_called_once()

		def test_draws_highlighted_sprite_if_highlighted(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.highlighted = True
			node.on_draw()
			node.sprite_highlighted.draw.assert_called_once()
    