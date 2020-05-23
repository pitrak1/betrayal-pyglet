import pyglet
import sys
from lattice2d.full.full_client import FullClientState, Renderer
from lattice2d.full.common import FullPlayerList
from lattice2d.utilities.pagination import get_page_info
from lattice2d.network import NetworkCommand
from lattice2d.nodes import Node
from src.client.client_components import Background, Area, Button, TextBox
from src.common import constants
from src.client.asset_manager import Assets
from src.client.client_game_states import ClientGameState
import config

class ClientSetupPlayerOrderState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.players = FullPlayerList()
		self.waiting = False
		super().__init__(set_state, add_command)
		self.add_command(NetworkCommand('network_get_player_order', status='pending'))
		
	def redraw(self):
		self.children = [
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 140, 
				unit_width=12, 
				unit_height=3, 
				text='Continue', 
				on_click=self.continue_,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]
		self.waiting_text = pyglet.text.Label(
			text='', 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 200, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(0)
		)
		self.other = [
			pyglet.text.Label(
				text='Welcome to Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			pyglet.text.Label(
				text='Turn order will be randomly determined', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 100, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			pyglet.text.Label(
				text='First player in the order will play first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 60, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			pyglet.text.Label(
				text='Last player in the order will choose their character first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 40, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			pyglet.text.Label(
				text='The player order is:', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 40, 
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
			self.other.append(pyglet.text.Label(
				text=player_text[:-2], 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 60, 
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
			self.set_state(ClientSetupCharacterSelectionState(self.set_state, self.add_command, self.player_name, self.game_name, self.host))


class CharacterTile(Node):
	def __init__(self, entry, x, y, active, batch, area_group, text_group, highlight_group):
		super().__init__()
		self.__area = Area(
			asset=Assets().common['area'], 
			x=x, 
			y=y + 60, 
			unit_width=16, 
			unit_height=24,
			batch=batch,
			group=area_group
		)
		self.__name_label = pyglet.text.Label(
			text=entry['display_name'], 
			x=x, 
			y=y + 230, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=15,
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__picture = pyglet.sprite.Sprite(
			Assets().characters[entry['variable_name']], 
			x=x, 
			y=y + 120, 
			batch=batch,
			group=text_group
		)

		speed_text = 'SPD: '
		for value in entry['speed']:
			speed_text += f'{value} '
		self.__speed_label = pyglet.text.Label(
			text=speed_text, 
			x=x, 
			y=y + 15, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__speed_indicator = pyglet.sprite.Sprite(
			Assets().common['attribute_highlight'], 
			x=x - 60 + 20 * entry['speed_index'], 
			y=y + 15, 
			batch=batch,
			group=highlight_group
		)

		might_text = 'MGT: '
		for value in entry['might']:
			might_text += f'{value} '
		self.__might_label = pyglet.text.Label(
			text=might_text, 
			x=x, 
			y=y - 25, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255),
			batch=batch,
			group=text_group
		)
		self.__might_indicator = pyglet.sprite.Sprite(
			Assets().common['attribute_highlight'], 
			x=x - 60 + 20 * entry['might_index'], 
			y=y - 25,
			batch=batch,
			group=highlight_group
		)

		sanity_text = 'SAN: '
		for value in entry['sanity']:
			sanity_text += f'{value} '
		self.__sanity_label = pyglet.text.Label(
			text=sanity_text, 
			x=x, 
			y=y - 65, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__sanity_indicator = pyglet.sprite.Sprite(
			Assets().common['attribute_highlight'], 
			x=x - 60 + 20 * entry['sanity_index'], 
			y=y - 65,
			batch=batch,
			group=highlight_group
		)

		knowledge_text = 'KNW: '
		for value in entry['knowledge']:
			knowledge_text += f'{value} '
		self.__knowledge_label = pyglet.text.Label(
			text=knowledge_text, 
			x=x, 
			y=y - 105, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=12, 
			font_name='Courier',
			color=(0, 0, 0, 255), 
			batch=batch,
			group=text_group
		)
		self.__knowledge_indicator = pyglet.sprite.Sprite(
			Assets().common['attribute_highlight'], 
			x=x - 60 + 20 * entry['knowledge_index'], 
			y=y - 105,
			batch=batch,
			group=highlight_group
		)

		if not active:
			self.__active_label = pyglet.text.Label(
				text='NOT ACTIVE', 
				x=x, 
				y=y + 215, 
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=12, 
				color=(0, 0, 0, 255), 
				batch=batch,
				group=text_group
			)

class ClientSetupCharacterSelectionState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.current_player = False
		self.character_index = 0
		self.available_characters = []
		self.title_text = ''
		super().__init__(set_state, add_command)
		self.add_command(NetworkCommand('network_get_available_characters', status='pending'))

	def redraw(self):
		self.children = [
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X-300, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=4, 
				unit_height=6, 
				text='Left', 
				on_click=self.go_left,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X+300, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=4, 
				unit_height=6, 
				text='Right', 
				on_click=self.go_right,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]

		self.title = pyglet.text.Label(
			text=self.title_text, 
			x=constants.WINDOW_CENTER_X, 
			y=constants.WINDOW_HEIGHT - 40, 
			anchor_x='center', 
			anchor_y='center', 
			align='center', 
			font_size=25, 
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(0)
		)
		self.other = [self.title]

		if config.CHARACTERS[self.character_index]['variable_name'] in self.available_characters:
			if self.current_player:
				self.children.append(Button(
					asset=Assets().common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y-250, 
					unit_width=12, 
					unit_height=3, 
					text='Select', 
					on_click=self.select_character,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(0),
					text_group=self.renderer.get_group(1)
				))
			self.children.append(CharacterTile(
				entry=config.CHARACTERS[self.character_index], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				active=True,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1),
				highlight_group=self.renderer.get_group(2)
			))
		else:
			self.children.append(CharacterTile(
				entry=config.CHARACTERS[self.character_index], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				active=False,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1),
				highlight_group=self.renderer.get_group(2)
			))

	def go_left(self):
		self.character_index -= 1
		if self.character_index < 0:
			self.character_index = len(config.CHARACTERS) - 1
		self.renderer = Renderer()
		self.redraw()

	def go_right(self):
		self.character_index += 1
		if self.character_index > len(config.CHARACTERS) - 1:
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
				{ 'character': config.CHARACTERS[self.character_index]['variable_name'] },
				'pending'
			))

	def network_all_characters_selected_handler(self, command):
		if command.status == 'success':
			self.set_state(ClientSetupCharacterOverviewState(self.set_state, self.add_command, self.player_name, self.game_name, self.host))


class ClientSetupCharacterOverviewState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.player_selections = []
		self.waiting = False
		super().__init__(set_state, add_command)
		self.add_command(NetworkCommand('network_get_character_selections', {}, 'pending'))
		
	def redraw(self):
		self.children = [
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 200, 
				unit_width=12, 
				unit_height=3, 
				text='Begin', 
				on_click=self.confirm_characters,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(0),
				text_group=self.renderer.get_group(1)
			)
		]
		self.waiting_label = pyglet.text.Label(
			text='', 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 260, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(0)
		)
		self.other = [
			pyglet.text.Label(
				text='The players\' selected characters are:', 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_HEIGHT - 40, 
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
				self.other.append(pyglet.text.Label(
					text=label_text, 
					x=constants.WINDOW_CENTER_X - 180, 
					y=constants.WINDOW_CENTER_Y + 130 - (40 * count), 
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
			self.set_state(ClientGameState(self.set_state, self.add_command, self.player_name, self.game_name, self.host))
