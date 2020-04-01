import sys
import pyglet
from src.client.world.common import button, text_box, area, background, label
from src.client.states import state
from src.client.states.menu import main_menu_state, game_state
from src.shared import constants, command

class CreateGameState(state.State):
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
					unit_width=40, 
					unit_height=30, 
					opacity=192,
					batch=self.batch,
					group=self.groups[1]
				),
				'title': label.Label(
					text='Create Game', 
					x=constants.WINDOW_CENTER_X,
					y=constants.WINDOW_CENTER_Y + 200,
					anchor_x='center', 
					anchor_y='center', 
					align='center', 
					font_size=25, 
					color=(0, 0, 0, 255),
					batch=self.batch,
					group=self.groups[2]
				),
				'game_name_input': text_box.TextBox(
					asset=self.asset_manager.common['text_box'], 
					x=constants.WINDOW_CENTER_X - 200, 
					y=constants.WINDOW_CENTER_Y + 50, 
					unit_width=26, 
					label_text='Game Name',
					max_length=40,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'back_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X - 150, 
					y=constants.WINDOW_CENTER_Y - 100, 
					unit_width=12, 
					unit_height=3, 
					text='Back', 
					on_click=self.back,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'create_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X + 150, 
					y=constants.WINDOW_CENTER_Y - 100, 
					unit_width=12, 
					unit_height=3, 
					text='Create', 
					on_click=self.create,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)
			}

	def back(self):
		self.set_state(main_menu_state.MainMenuState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			testing=self.testing
		))

	def invalid_game_name(self):
		self.elements['game_name_input'].set_error_text('name is already in use')

	def name_too_short(self):
		self.elements['game_name_input'].set_error_text('must be 6 characters or more')

	def name_too_long(self):
		self.elements['game_name_input'].set_error_text('must be 40 characters or less')

	def create(self):
		game_name = self.elements['game_name_input'].get_text()
		if len(game_name) < 6:
			self.elements['game_name_input'].set_error_text('must be 6 characters or more')
		else:
			self.add_command(command.Command('network_create_game', { 'status': 'pending', 'game_name': game_name }))

	def next(self, game_name):
		self.set_state(game_state.GameState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			game_name,
			True,
			testing=self.testing
		))
