from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, TextBox, Label
from lattice2d.command import Command
from constants import WINDOW_CENTER

class CreateGameState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(20, 15)
		))
		self.register_component('name_text_box', 'ui', TextBox(
		    position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 50), 
			unit_width=13, 
			label_text='Game Name',
			max_length=40
		))
		self.register_component('back_button', 'ui', Button(
			position=(WINDOW_CENTER[0] - 150, WINDOW_CENTER[1] - 100),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.back
		))
		self.register_component('create_button', 'ui', Button(
			position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 100),
			unit_dimensions=(12, 3),
			text='Create',
			on_click=self.create
		))
		self.register_component('title', 'ui', Label(
			text='Create Game',
			x=WINDOW_CENTER[0],
			y=WINDOW_CENTER[1] + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			font_size=25,
			color=(0, 0, 0, 255)
		))
		
	def back(self):
		self.to_main_menu_state(self.custom_data)

	def create(self):
		game_name = self.get_component('name_text_box').get_text()
		if len(game_name) < 6:
			self.get_component('name_text_box').set_error_text('must be >5 characters')
		else:
			self.add_command(Command('create_game', { 'game_name': game_name }, 'pending'))

	def create_game_handler(self, command):
		if command.status == 'invalid_name':
			self.get_component('name_text_box').set_error_text('name is taken')
		elif command.status == 'name_too_short':
			self.get_component('name_text_box').set_error_text('must be >5 characters')
		elif command.status == 'name_too_long':
			self.get_component('name_text_box').set_error_text('must be <41 characters')
		else:
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': True })
			self.to_lobby_state(self.custom_data)