import sys
from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, TextBox, Label
from lattice2d.command import Command
from constants import WINDOW_CENTER


class CreatePlayerState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(10, 15)
		))
		self.register_component('name_input', 'environment', TextBox(
			position=(WINDOW_CENTER[0] - 120, WINDOW_CENTER[1] + 50),
			unit_width=8,
			label_text='Player Name',
			max_length=23
		))
		self.register_component('continue_button', 'environment', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 50),
			unit_dimensions=(12, 3),
			text='Continue',
			on_click=self.continue_
		))
		self.register_component('exit_button', 'environment', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 110),
			unit_dimensions=(12, 3),
			text='Exit',
			on_click=self.exit
		))
		self.register_component('title', 'environment', Label(
			text='Betrayal Online',
			font_size=25,
			x=WINDOW_CENTER[0],
			y=WINDOW_CENTER[1] + 150,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))

	def exit(self):
		sys.exit()

	def continue_(self):
		player_name = self.get_component('name_input').get_text()
		if len(player_name) < 6:
			self.get_component('name_input').set_error_text('must be >5 characters')
		else:
			self.add_command(Command('create_player', { 'player_name': player_name }, 'pending'))

	def create_player_handler(self, command):
		if command.status == 'name_too_short':
			self.get_component('name_input').set_error_text('must be >5 characters')
		elif command.status == 'name_too_long':
			self.get_component('name_input').set_error_text('must be <26 characters')
		elif command.status == 'invalid_name':
			self.get_component('name_input').set_error_text('name is taken')
		elif command.status == 'success':
			self.to_main_menu_state({ 'player_name': command.data['player_name'] })