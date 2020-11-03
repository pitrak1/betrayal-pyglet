from lattice2d.client import ClientState
from lattice2d.components import Button, Label
from lattice2d.command import Command
from constants import WINDOW_CENTER

class PlayerOrderState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.players = []
		self.waiting = False
		super().__init__(add_command, custom_data)
		self.add_command(Command('network_get_player_order', status='pending'))
		
	def redraw(self):
		self.children = [
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] - 140), 
				unit_dimensions=(12, 3), 
				text='Continue', 
				on_click=self.continue_,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]
		self.waiting_text = Label(
			text='', 
			x=WINDOW_CENTER[0] - 220, 
			y=WINDOW_CENTER[1] - 200, 
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
				text='Welcome to Betrayal Online',
				font_size=25,
				x=WINDOW_CENTER[0], 
				y=WINDOW_CENTER[1] + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Label(
				text='Turn order will be randomly determined', 
				x=WINDOW_CENTER[0] - 220, 
				y=WINDOW_CENTER[1] + 100, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Label(
				text='First player in the order will play first.', 
				x=WINDOW_CENTER[0] - 220, 
				y=WINDOW_CENTER[1] + 60, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Label(
				text='Last player in the order will choose their character first.', 
				x=WINDOW_CENTER[0] - 220, 
				y=WINDOW_CENTER[1] + 40, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Label(
				text='The player order is:', 
				x=WINDOW_CENTER[0] - 220, 
				y=WINDOW_CENTER[1] - 40, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			self.waiting_text
		]

		if len(self.players) > 0:
			player_text = ''
			for player in self.players:
				player_text += player
				player_text += ', '
			self.other.append(Label(
				text=player_text[:-2], 
				x=WINDOW_CENTER[0] - 220, 
				y=WINDOW_CENTER[1] - 60, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			))

	def network_get_player_order_handler(self, command):
		if command.status == 'success':
			self.players = command.data['players']
			self.renderer = Renderer()
			self.redraw()

	def continue_(self):
		if not self.waiting:
			self.waiting = True
			self.waiting_text.text = 'Waiting for other players...'
			self.add_command(NetworkCommand('network_confirm_player_order', status='pending'))

	def network_confirm_player_order_handler(self, command):
		if command.status == 'success':
			self.to_character_selection_state(self.custom_data)
