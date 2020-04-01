import sys
import pyglet
from src.client.world.common import background, button, area, label
from src.client.states import state
from src.client.states.menu import create_game_state, game_list_state
from src.shared import constants, command

class MainMenuState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
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
				'create_button': button.Button(
					asset=self.asset_manager.common['button'],
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y + 50, 
					unit_width=12, 
					unit_height=3, 
					text='Create Game', 
					on_click=self.create_game,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'join_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y - 30, 
					unit_width=12, 
					unit_height=3,
					text='Join Game', 
					on_click=self.join_game,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'exit_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y - 110, 
					unit_width=12, 
					unit_height=3, 
					text='Exit', 
					on_click=self.start_exit,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)
			}

	def start_exit(self):
		self.add_command(command.Command('network_logout', { 'status': 'pending' }))

	def exit(self):
		sys.exit()

	def create_game(self):
		self.set_state(create_game_state.CreateGameState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			testing=self.testing
		))

	def join_game(self):
		self.set_state(game_list_state.GameListState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			testing=self.testing
		))

	

