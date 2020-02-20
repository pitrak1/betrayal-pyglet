import pytest
import pyglet

@pytest.mark.usefixtures('make_tile')
class TestTile():
	class TestOnDraw():
		def test_draws_selected_sprite_if_selected(self, mocker, make_tile):
			tile = make_tile(mocker)
			tile.on_draw(True)
			tile.selected.draw.assert_called_once()

		def test_does_not_draw_selected_sprite_if_not_selected(self, mocker, make_tile):
			tile = make_tile(mocker)
			tile.on_draw(False)
			tile.selected.draw.assert_not_called()

	class TestWithinBounds():
		def test_raises_exception(self, mocker, make_tile):
			tile = make_tile(mocker)
			with pytest.raises(NotImplementedError) as exception:
				tile.within_bounds('position')
			assert str(exception.value) == 'within_bounds must be overridden'
    