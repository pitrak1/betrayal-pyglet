import sys
from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.area import Area
from lattice2d.client.components.button import Button
from lattice2d.client.components.text_box import TextBox
from lattice2d.client.components.label import Label
from lattice2d.network.network_command import NetworkCommand
from constants import WINDOW_CENTER


class CreatePlayerState(ClientState):
	def redraw(self):
		self.player_name_input = TextBox(
			position=(WINDOW_CENTER[0] - 120, WINDOW_CENTER[1] + 50), 
			unit_width=8,
			label_text='Player Name',
			max_length=25,
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
				unit_dimensions=(10, 15),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			self.player_name_input,
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 50), 
				unit_dimensions=(12, 3), 
				text='Continue', 
				on_click=self.continue_,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 110), 
				unit_dimensions=(12, 3),
				text='Exit', 
				on_click=self.exit,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Label(
				text='Betrayal Online',
				font_size=25,
				x=WINDOW_CENTER[0], 
				y=WINDOW_CENTER[1] + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			)
		]

	def exit(self):
		sys.exit()

	def continue_(self):
		player_name = self.player_name_input.get_text()
		if len(player_name) < 6:
			self.player_name_input.set_error_text('must be 6 characters or more')
		else:
			self.add_command(NetworkCommand('create_player', { 'player_name': player_name }, 'pending'))

	def create_player_handler(self, command):
		if command.status == 'name_too_short':
			self.player_name_input.set_error_text('must be 6 characters or more')
		elif command.status == 'name_too_long':
			self.player_name_input.set_error_text('must be 25 characters or less')
		elif command.status == 'invalid_name':
			self.player_name_input.set_error_text('name is already in use')
		elif command.status == 'success':
			self.to_main_menu_state({ 'player_name': command.data['player_name'] })