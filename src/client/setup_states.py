import pyglet
import sys
from lattice2d.client import ClientState
from lattice2d.components import Button, Label
from lattice2d.command import Command
from constants import WINDOW_CENTER, WINDOW_DIMENSIONS, CHARACTERS
from src.client.components import CharacterTile

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


class CharacterSelectionState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.current_player = False
		self.character_index = 0
		self.available_characters = []
		self.title_text = ''
		super().__init__(add_command, custom_data)
		self.add_command(NetworkCommand('network_get_available_characters', status='pending'))

	def redraw(self):
		self.children = [
			Button(
				position=(WINDOW_CENTER[0]-300, WINDOW_CENTER[1]), 
				unit_dimensions=(4, 6), 
				text='Left', 
				on_click=self.go_left,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			),
			Button(
				position=(WINDOW_CENTER[0]+300, WINDOW_CENTER[1]), 
				unit_dimensions=(4, 6), 
				text='Right', 
				on_click=self.go_right,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]

		self.title = pyglet.text.Label(
			text=self.title_text, 
			x=WINDOW_CENTER[0], 
			y=WINDOW_DIMENSIONS[1] - 40, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=25, 
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(0)
		)
		self.other = [self.title]

		if CHARACTERS[self.character_index]['variable_name'] in self.available_characters:
			if self.current_player:
				self.children.append(Button(
					position=(WINDOW_CENTER[0], WINDOW_CENTER[1]-250), 
					unit_dimensions=(12, 3), 
					text='Select', 
					on_click=self.select_character,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(0),
					text_group=self.renderer.get_group(1)
				))
			self.children.append(CharacterTile(
				entry=CHARACTERS[self.character_index], 
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]), 
				active=True,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1),
				highlight_group=self.renderer.get_group(2)
			))
		else:
			self.children.append(CharacterTile(
				entry=CHARACTERS[self.character_index], 
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]), 
				active=False,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1),
				highlight_group=self.renderer.get_group(2)
			))

	def go_left(self):
		self.character_index -= 1
		if self.character_index < 0:
			self.character_index = len(CHARACTERS) - 1
		self.renderer = Renderer()
		self.redraw()

	def go_right(self):
		self.character_index += 1
		if self.character_index > len(CHARACTERS) - 1:
			self.character_index = 0
		self.renderer = Renderer()
		self.redraw()

	def network_get_available_characters_handler(self, command):
		if command.status == 'success':
			self.available_characters = command.data['characters']
			self.renderer = Renderer()
			self.redraw()
			self.add_command(NetworkCommand('get_current_player', status='pending'))

	def get_current_player_handler(self, command):
		if command.status == 'success':
			player_name = command.data['player_name']
			if player_name == 'self':
				self.title_text = 'You are choosing'
				self.current_player = True
			else:
				self.title_text = f'{player_name} is choosing'
				self.current_player = False
			self.renderer = Renderer()
			self.redraw()

	def select_character(self):
		if self.current_player:
			self.add_command(NetworkCommand(
				'network_select_character', 
				{ 'character': CHARACTERS[self.character_index]['variable_name'] },
				'pending'
			))

	def network_all_characters_selected_handler(self, command):
		if command.status == 'success':
			self.to_character_overview_state(self.custom_data)



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
				unit_dimensions=(12, 3), 
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
			self.to_game_base_state(self.custom_data)
