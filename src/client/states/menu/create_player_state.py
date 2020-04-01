import sys
import pyglet
from src.client.world.common import background, button, text_box, area, label
from src.client.states import state
from src.client.states.menu import main_menu_state
from src.shared import constants, command

class CreatePlayerState(state.State):
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
				'player_name_input': text_box.TextBox(
					asset=self.asset_manager.common['text_box'], 
					x=constants.WINDOW_CENTER_X - 120, 
					y=constants.WINDOW_CENTER_Y + 50, 
					unit_width=16,
					label_text='Player Name',
					max_length=25,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'continue_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y - 50, 
					unit_width=12, 
					unit_height=3, 
					text='Continue', 
					on_click=self.continue_,
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
					on_click=self.exit,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)
			}

	def exit(self):
		sys.exit()

	def continue_(self):
		player_name = self.elements['player_name_input'].get_text()
		if len(player_name) < 6:
			self.elements['player_name_input'].set_error_text('must be 6 characters or more')
		else:
			self.add_command(command.Command('network_create_player', { 'status': 'pending', 'player_name': player_name }))

	def invalid_player_name(self):
		self.elements['player_name_input'].set_error_text('name is already in use')

	def name_too_short(self):
		self.elements['player_name_input'].set_error_text('must be 6 characters or more')

	def name_too_long(self):
		self.elements['player_name_input'].set_error_text('must be 25 characters or less')

	def next(self, player_name):
		self.set_state(main_menu_state.MainMenuState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			player_name,
			testing=self.testing
		))
