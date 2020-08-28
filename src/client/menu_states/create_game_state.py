from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.area import Area
from lattice2d.client.components.button import Button
from lattice2d.client.components.text_box import TextBox
from lattice2d.client.components.label import Label
from lattice2d.network.network_command import NetworkCommand
from constants import WINDOW_CENTER

class CreateGameState(ClientState):
	def redraw(self):
		self.game_name_input = TextBox(
			position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 50), 
			unit_width=13, 
			label_text='Game Name',
			max_length=40,
			batch=self.renderer.get_batch(),
			area_group=self.renderer.get_group(2),
			text_group=self.renderer.get_group(3)
		)
		self.children = [
			Background(
				asset_key='menu_background',
				batch=self.renderer.get_batch(),	
				group=self.renderer.get_group(0)
			),
			Area(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]), 
				unit_dimensions=(20, 15), 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			self.game_name_input,
			Button(
				position=(WINDOW_CENTER[0] - 150, WINDOW_CENTER[1] - 100), 
				unit_dimensions=(12, 3), 
				text='Back', 
				on_click=self.back,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 100), 
				unit_dimensions=(12, 3), 
				text='Create', 
				on_click=self.create,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Label(
				text='Create Game', 
				x=WINDOW_CENTER[0],
				y=WINDOW_CENTER[1] + 200,
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			)
		]

	def back(self):
		self.to_main_menu_state(self.custom_data)

	def create(self):
		game_name = self.game_name_input.get_text()
		if len(game_name) < 6:
			self.game_name_input.set_error_text('must be 6 characters or more')
		else:
			self.add_command(NetworkCommand('create_game', { 'game_name': game_name }, 'pending'))

	def create_game_handler(self, command):
		if command.status == 'invalid_name':
			self.game_name_input.set_error_text('name is already in use')
		elif command.status == 'name_too_short':
			self.game_name_input.set_error_text('must be 6 characters or more')
		elif command.status == 'name_too_long':
			self.game_name_input.set_error_text('must be 40 characters or less')
		else:
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': True })
			self.to_lobby_state(self.custom_data)