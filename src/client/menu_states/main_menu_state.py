import sys
from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, Label
from lattice2d.command import Command
from constants import WINDOW_CENTER

class MainMenuState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(10, 15)
		))
		self.register_component('create_button', 'ui', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] + 50),
			unit_dimensions=(12, 3),
			text='Create Game',
			on_click=self.create_game
		))
		self.register_component('join_button', 'ui', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 30),
			unit_dimensions=(12, 3),
			text='Join Game',
			on_click=self.join_game
		))
		self.register_component('exit_button', 'ui', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 110),
			unit_dimensions=(12, 3),
			text='Exit',
			on_click=self.exit
		))
		self.register_component('title', 'ui', Label(
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
		self.add_command(Command('logout', status='pending'))

	def logout_handler(self, command):
		if command.status == 'success':
			sys.exit()

	def create_game(self):
		self.to_create_game_state(self.custom_data)

	def join_game(self):
		self.to_join_game_state(self.custom_data)
