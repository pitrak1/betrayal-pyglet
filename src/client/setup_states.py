import pyglet
import sys
from lattice2d.client import ClientState
from lattice2d.components import Button, Label, UnformattedText
from lattice2d.command import Command
from constants import Constants
from src.client.components import CharacterTile

class PlayerOrderState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.__waiting = False
		self.add_command(Command('get_player_order', status='pending'))
		self.register_component('continue_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 140), 
			unit_dimensions=(12, 3), 
			text='Continue', 
			on_click=self.continue_
		))
		self.register_component('waiting_text', 'ui', Label(
			text='', 
			x=Constants.window_center_x - 220, 
			y=Constants.window_center_y - 200, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))
		self.register_component('title', 'ui', Label(
			text='Welcome to Betrayal Online',
			font_size=25,
			x=Constants.window_center_x, 
			y=Constants.window_center_y + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 255, 255, 255)
		))
		self.info_text = UnformattedText(
			pyglet.text.document.UnformattedDocument(), 
			multiline=True,
			wrap_lines=False
		)
		self.info_text.set_style({ 'color': (255, 255, 255, 255), 'font_size': 18 })
		self.info_text.set_position((Constants.window_center_x - 220, Constants.window_center_y + 100), 'left', 'center')
		self.register_component('selections', 'ui', self.info_text)
		self.info_text.set_text('Turn order will be randomly determined.\n'\
			'First player in the order will play first.\n'\
			'Last player in the order will choose their character first.'
		)
		self.register_component('player_order_label', 'ui', Label(
			text='The player order is:', 
			x=Constants.window_center_x - 220, 
			y=Constants.window_center_y - 40, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))
		self.register_component('player_order_text', 'ui', Label(
			text='', 
			x=Constants.window_center_x - 220, 
			y=Constants.window_center_y - 60, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))

	def get_player_order_handler(self, command):
		if command.status == 'success':
			players = command.data['players']
			if len(players) > 0:
				player_text = ''
				for player in players:
					player_text += player
					player_text += ', '
				self.get_component('player_order_text').text = player_text[:-2]

	def continue_(self):
		if not self.__waiting:
			self.__waiting = True
			self.get_component('waiting_text').text = 'Waiting for other players...'
			self.add_command(Command('confirm_player_order', status='pending'))

	def confirm_player_order_handler(self, command):
		if command.status == 'success':
			self.to_character_selection_state(self.custom_data)


class CharacterSelectionState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.__current_player = False
		self.__character_index = 0
		self.__available_characters = []
		self.add_command(Command('get_available_characters', status='pending'))
		self.register_component('left_button', 'ui', Button(
			position=(Constants.window_center_x-300, Constants.window_center_y), 
			unit_dimensions=(4, 6), 
			text='Left', 
			on_click=self.go_left
		))
		self.register_component('right_button', 'ui', Button(
			position=(Constants.window_center_x+300, Constants.window_center_y), 
			unit_dimensions=(4, 6), 
			text='Right', 
			on_click=self.go_right
		))
		self.register_component('title', 'ui', Label(
			text='', 
			x=Constants.window_center_x, 
			y=Constants.window_dimensions_y - 40, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=25, 
			color=(255, 255, 255, 255)
		))

	def redraw_tile(self):
		self.conditionally_remove_component('character_tile')
		self.register_component('character_tile', 'ui', CharacterTile(
			entry=Constants.characters[self.__character_index], 
			position=(Constants.window_center_x, Constants.window_center_y), 
			active=self.character_available()
		))

	def go_left(self):
		self.__character_index -= 1
		if self.__character_index < 0:
			self.__character_index = len(Constants.characters) - 1
		self.redraw_tile()

	def go_right(self):
		self.__character_index += 1
		if self.__character_index > len(Constants.characters) - 1:
			self.__character_index = 0
		self.redraw_tile()

	def get_available_characters_handler(self, command):
		if command.status == 'success':
			self.__available_characters = command.data['characters']
			self.add_command(Command('get_current_player', status='pending'))

	def get_current_player_handler(self, command):
		if command.status == 'success':
			player_name = command.data['player_name']
			if player_name == 'self':
				self.get_component('title').text = 'You are choosing'
				self.__current_player = True
				self.register_component('select_button', 'ui', Button(
					position=(Constants.window_center_x, Constants.window_center_y-250), 
					unit_dimensions=(12, 3), 
					text='Select', 
					on_click=self.select_character
				))
			else:
				self.get_component('title').text = f'{player_name} is choosing'
				self.__current_player = False
				self.conditionally_remove_component('select_button')
			self.redraw_tile()

	def character_available(self):
		return Constants.characters[self.__character_index]['key'] in self.__available_characters

	def select_character(self):
		if self.__current_player and self.character_available():
			self.add_command(Command(
				'select_character', 
				{ 'character': Constants.characters[self.__character_index]['key'] },
				'pending'
			))

	def all_characters_selected_handler(self, command):
		if command.status == 'success':
			self.to_character_overview_state(self.custom_data)



class CharacterOverviewState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.player_selections = []
		self.waiting = False
		self.add_command(Command('get_character_selections', {}, 'pending'))
		self.register_component('confirm_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 200), 
			unit_dimensions=(12, 3), 
			text='Begin', 
			on_click=self.confirm_characters
		))
		self.register_component('waiting_text', 'ui', Label(
			text='', 
			x=Constants.window_center_x - 220, 
			y=Constants.window_center_y - 260, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))
		self.register_component('info_1', 'ui', Label(
			text='The players\' selected Constants.characters are:', 
			x=Constants.window_center_x, 
			y=Constants.window_dimensions_y - 40, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=25, 
			color=(255, 255, 255, 255)
		))

		self.selections_text = UnformattedText(
			pyglet.text.document.UnformattedDocument(), 
			multiline=True,
			wrap_lines=False
		)
		self.selections_text.set_style({ 'color': (255, 255, 255, 255), 'font_size': 18 })
		self.selections_text.set_position((Constants.window_center_x - 180, Constants.window_center_y + 130), 'left', 'center')
		self.register_component('selections', 'ui', self.selections_text)

	def get_character_selections_handler(self, command):
		if command.status == 'success':
			self.player_selections = command.data['selections']
			label_text = ''
			for selection in self.player_selections:
				label_text += f'{selection[0]}: {selection[1]}\n'
			self.selections_text.set_text(label_text)

	def confirm_characters(self):
		if not self.waiting:
			self.waiting = True
			self.get_component('waiting_text').text = 'Waiting for other players...'
			self.add_command(Command('confirm_character_selections', {}, 'pending'))

	def confirm_character_selections_handler(self, command):
		if command.status == 'success':
			self.to_game_base_state(self.custom_data)
