import pyglet
import sys
from lattice2d.client import ClientState
from lattice2d.components import Button, Label
from lattice2d.command import Command
from src.client.setup_states.character_tile import CharacterTile
from constants import WINDOW_CENTER, WINDOW_DIMENSIONS, CHARACTERS

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