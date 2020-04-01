import pyglet
from src.client.world.common import background, button, area, label
from src.client.states import state
from src.client.states.menu import create_player_state
from src.shared import constants

class SplashState(state.State):
	def __init__(self, asset_manager, set_state, add_command, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.redraw()

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
			self.elements = {
				'background': background.Background(
					asset=self.asset_manager.common['menu_background'],
					batch=self.batch, 
					group=self.groups[0]
				),
				'border': area.Area(
					asset=self.asset_manager.common['area'],
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y, 
					unit_width=20, 
					unit_height=30,
					batch=self.batch,
					group=self.groups[1],
					opacity=192
				),
				'title': label.Label(
					text='Betrayal Online',
					font_size=25,
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y + 150,
					anchor_x='center',
					anchor_y='center',
					align='center',
					color=(0, 0, 0, 255),
					batch=self.batch,
					group=self.groups[2]
				),
				'begin_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y + 50,
					unit_width=12,
					unit_height=3,
					text='Begin', 
					on_click=self.begin,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)
			}


	def begin(self):
		self.set_state(create_player_state.CreatePlayerState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.testing
		))
