from lattice2d.client.client_state import ClientState
from lattice2d.client.components.button import Button
from lattice2d.client.components.label import Label
from lattice2d.network.network_command import NetworkCommand
from constants import WINDOW_CENTER, WINDOW_DIMENSIONS

class CharacterOverviewState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.player_selections = []
		self.waiting = False
		super().__init__(add_command, custom_data)
		self.add_command(NetworkCommand('network_get_character_selections', {}, 'pending'))
		
	def redraw(self):
		self.children = [
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 200), 
				unit_dimensions=(6, 2), 
				text='Begin', 
				on_click=self.confirm_characters,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]
		self.waiting_label = Label(
			text='', 
			x=WINDOW_CENTER[0] - 220, 
			y=WINDOW_CENTER[1] - 260, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(0)
		)
		self.other = [
			Label(
				text='The players\' selected characters are:', 
				x=WINDOW_CENTER[0], 
				y=WINDOW_DIMENSIONS[1] - 40, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			self.waiting_label
		]

		if len(self.player_selections) > 0:
			count = 0
			for selection in self.player_selections:
				label_text = f'{selection[0]}: {selection[1]}'
				self.other.append(Label(
					text=label_text, 
					x=WINDOW_CENTER[0] - 180, 
					y=WINDOW_CENTER[1] + 130 - (40 * count), 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=18, 
					color=(255, 255, 255, 255),
					batch=self.renderer.get_batch(),
					group=self.renderer.get_group(0)
				))
				count += 1

	def network_get_character_selections_handler(self, command):
		if command.status == 'success':
			self.player_selections = command.data['selections']
			self.redraw()

	def confirm_characters(self):
		if not self.waiting:
			self.waiting = True
			self.waiting_label.text = 'Waiting for other players...'
			self.add_command(NetworkCommand('network_confirm_character_selections', {}, 'pending'))

	def network_confirm_character_selections_handler(self, command):
		if command.status == 'success':
			print('confirmed')
			# self.set_state(ClientGameState(self.set_state, self.add_command, self.player_name, self.game_name, self.host))
