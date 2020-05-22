import pyglet
import sys
from lattice2d.full.full_client import FullClientState, Renderer
from lattice2d.full.full_server import FullServerPlayerList
from lattice2d.utilities.pagination import get_page_info
from lattice2d.network import NetworkCommand
from lattice2d.nodes import Node
from src.client.client_components import Background, Area, Button, TextBox
from src.common import constants
from src.client.asset_manager import Assets
from src.client.client_setup_states import ClientSetupPlayerOrderState

class ClientMenuSplashState(FullClientState):
	def redraw(self):
		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(), 
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'],
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=20, 
				unit_height=30,
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 50,
				unit_width=12,
				unit_height=3,
				text='Begin', 
				on_click=self.begin,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.other = [
			pyglet.text.Label(
				text='Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			)
		]

	def begin(self):
		self.set_state(ClientMenuCreatePlayerState(self.set_state, self.add_command))


class ClientMenuCreatePlayerState(FullClientState):
	def redraw(self):
		self.player_name_input = TextBox(
			asset=Assets().common['text_box'], 
			x=constants.WINDOW_CENTER_X - 120, 
			y=constants.WINDOW_CENTER_Y + 50, 
			unit_width=16,
			label_text='Player Name',
			max_length=25,
			batch=self.renderer.get_batch(),
			area_group=self.renderer.get_group(2),
			text_group=self.renderer.get_group(3)
		)

		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'],
				x=constants.WINDOW_CENTER_X,
				y=constants.WINDOW_CENTER_Y,
				unit_width=20,
				unit_height=30,
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			self.player_name_input,
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 50, 
				unit_width=12, 
				unit_height=3, 
				text='Continue', 
				on_click=self.continue_,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 110, 
				unit_width=12, 
				unit_height=3, 
				text='Exit', 
				on_click=self.exit,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.other = [
			pyglet.text.Label(
				text='Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 150,
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
			self.set_state(ClientMenuMainMenuState(self.set_state, self.add_command, command.data['player_name']))


class ClientMenuMainMenuState(FullClientState):
	def __init__(self, set_state, add_command, player_name):
		super().__init__(set_state, add_command)
		self.player_name = player_name

	def redraw(self):
		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=20, 
				unit_height=30,
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				asset=Assets().common['button'],
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 50, 
				unit_width=12, 
				unit_height=3, 
				text='Create Game', 
				on_click=self.create_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 30, 
				unit_width=12, 
				unit_height=3,
				text='Join Game', 
				on_click=self.join_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 110, 
				unit_width=12, 
				unit_height=3, 
				text='Exit', 
				on_click=self.exit,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.other = [
			pyglet.text.Label(
				text='Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
		]

	def exit(self):
		self.add_command(NetworkCommand('logout', status='pending'))

	def logout_handler(self, command):
		if command.status == 'success':
			sys.exit()

	def create_game(self):
		self.set_state(ClientMenuCreateGameState(self.set_state, self.add_command, self.player_name))

	def join_game(self):
		self.set_state(ClientMenuGameListState(self.set_state, self.add_command, self.player_name))


class ClientMenuCreateGameState(FullClientState):
	def __init__(self, set_state, add_command, player_name):
		super().__init__(set_state, add_command)
		self.player_name = player_name

	def redraw(self):
		self.game_name_input = TextBox(
			asset=Assets().common['text_box'], 
			x=constants.WINDOW_CENTER_X - 200, 
			y=constants.WINDOW_CENTER_Y + 50, 
			unit_width=26, 
			label_text='Game Name',
			max_length=40,
			batch=self.renderer.get_batch(),
			area_group=self.renderer.get_group(2),
			text_group=self.renderer.get_group(3)
		)
		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(),	
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=40, 
				unit_height=30, 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			self.game_name_input,
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X - 150, 
				y=constants.WINDOW_CENTER_Y - 100, 
				unit_width=12, 
				unit_height=3, 
				text='Back', 
				on_click=self.back,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 100, 
				unit_width=12, 
				unit_height=3, 
				text='Create', 
				on_click=self.create,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.other = [
			pyglet.text.Label(
				text='Create Game', 
				x=constants.WINDOW_CENTER_X,
				y=constants.WINDOW_CENTER_Y + 200,
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
		self.set_state(ClientMenuMainMenuState(self.set_state, self.add_command, self.player_name))

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
			self.set_state(ClientMenuLobbyState(self.set_state, self.add_command, self.player_name, command.data['game_name'], True))

class GameListing(Node):
	def __init__(self, name, players, x, y, on_click, batch, area_group, text_group):
		super().__init__()
		self.name = name
		self.__area = Area(
			asset=Assets().common['button'], 
			x=x, 
			y=y, 
			unit_width=26, 
			unit_height=2, 
			align='left',
			batch=batch,
			group=area_group
		)
		self.__game_name = pyglet.text.Label(
			text=name, 
			x=x, 
			y=y, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		self.__player_count = pyglet.text.Label(
			text=f'{players}/{constants.PLAYERS_PER_GAME}', 
			x=x + 390, 
			y=y, 
			anchor_x='right', 
			anchor_y='center', 
			align='right', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		self.__on_click = on_click

	def mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds(command.data['x'], command.data['y']):
			self.__on_click()	

class ClientMenuGameListState(FullClientState):
	def __init__(self, set_state, add_command, player_name):
		self.current_page = 0
		self.available_games = []
		self.available_games_count = 0
		super().__init__(set_state, add_command)
		self.player_name = player_name
		self.add_command(NetworkCommand('get_games', status='pending'))

	def redraw(self):
		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=40, 
				unit_height=30, 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X - 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Back', 
				on_click=self.back,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Refresh', 
				on_click=self.refresh,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.error_text = pyglet.text.Label(
			text='',
			font_size=15,
			x=constants.WINDOW_CENTER_X + 150, 
			y=constants.WINDOW_CENTER_Y - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(2)
		)
		self.other = [
			pyglet.text.Label(
				text='Games',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			self.error_text
		]

		if self.available_games_count > 0:
			min_, max_, down, up = get_page_info(
				self.current_page, 
				constants.GAME_LIST_PAGE_SIZE, 
				self.available_games_count
			)

			count = 0
			for game in self.available_games[min_:max_]:
				if game == '': break
				self.children.append(GameListing(
					name=game[0], 
					players=game[1], 
					x=constants.WINDOW_CENTER_X - 200, 
					y=constants.WINDOW_CENTER_Y + 120 - 40 * (count % constants.GAME_LIST_PAGE_SIZE), 
					on_click=lambda : self.join(game[0], int(game[1])),
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))
				count += 1

			if down:
				self.elements.append(Button(
					asset=Assets().common['button'], 
					x=constants.WINDOW_CENTER_X + 250, 
					y=constants.WINDOW_CENTER_Y - 50, 
					unit_width=3, 
					unit_height=5, 
					text='Down', 
					on_click=self.go_forward_page,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))

			if up:
				self.elements.append(Button(
					asset=Assets().common['button'], 
					x=constants.WINDOW_CENTER_X + 250, 
					y=constants.WINDOW_CENTER_Y + 50, 
					unit_width=3, 
					unit_height=5, 
					text='Up', 
					on_click=self.go_back_page,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))

	def get_games_handler(self, command):
		if command.status == 'success':
			self.available_games = command.data['games']
			self.available_games_count = len(command.data['games'])
			self.renderer = Renderer()
			self.redraw()

	def go_forward_page(self):
		self.current_page += 1
		self.renderer = Renderer()
		self.redraw()

	def go_back_page(self):
		self.current_page -= 1
		self.renderer = Renderer()
		self.redraw()

	def refresh(self):
		self.add_command(NetworkCommand('get_games', status='pending'))

	def back(self):
		self.set_state(ClientMenuMainMenuState(self.set_state, self.add_command, self.player_name))

	def join(self, game, number_of_players):
		if number_of_players >= constants.PLAYERS_PER_GAME:
			self.error_text.text = 'Game is full'
		else:
			self.add_command(NetworkCommand('join_game', { 'game_name': game }, 'pending'))

	def join_game_handler(self, command):
		if command.status == 'game_full':
			self.error_text.text = 'Game is full'
		elif command.status == 'success':
			self.set_state(ClientMenuLobbyState(self.set_state, self.add_command, self.player_name, command.data['game_name'], False))

class GamePlayer(Node):
	def __init__(self, name, host, x, y, batch, area_group, text_group):
		super().__init__()
		self.__area = Area(
			asset=Assets().common['button'], 
			x=x, 
			y=y, 
			unit_width=26, 
			unit_height=2, 
			align='left',
			batch=batch,
			group=area_group
		)
		self.__player_name = pyglet.text.Label(
			text=name, 
			x=x, 
			y=y, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15,
			batch=batch,
			group=text_group
		)
		if host:
			self.__crown = pyglet.sprite.Sprite(
				Assets().common['host_marker'], 
				x=x + 390, 
				y=y,
				batch=batch,
				group=text_group
			)

class ClientMenuLobbyState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.players = FullServerPlayerList()
		super().__init__(set_state, add_command)
		self.add_command(NetworkCommand('broadcast_players_in_game', status='pending'))

	def redraw(self):
		self.children = [
			Background(
				asset=Assets().common['menu_background'],
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Area(
				asset=Assets().common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=40, 
				unit_height=30, 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X - 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Back', 
				on_click=self.leave_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
		self.error_text = pyglet.text.Label(
			text='',
			font_size=15,
			x=constants.WINDOW_CENTER_X + 150, 
			y=constants.WINDOW_CENTER_Y - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(2)
		)
		self.other = [
			pyglet.text.Label(
				text=self.game_name,
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			self.error_text
		]

		if self.host:
			self.children.append(Button(
				asset=Assets().common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Start', 
				on_click=self.start_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			))

		count = 0
		for player in self.players:
			self.children.append(GamePlayer(
				name=player[0], 
				host=player[1], 
				x=constants.WINDOW_CENTER_X - 200, 
				y=constants.WINDOW_CENTER_Y + 120 - 40 * count,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			))
			count += 1

	def broadcast_players_in_game_handler(self, command):
		if command.status == 'success':
			self.players = command.data['players']
			self.renderer = Renderer()
			self.redraw()

	def leave_game(self):
		self.add_command(NetworkCommand('leave_game', status='pending'))

	def leave_game_handler(self, command):
		if command.status == 'success':
			self.set_state(ClientMenuMainMenuState(self.set_state, self.add_command, self.player_name))

	def start_game(self):
		if len(self.players) < constants.MINIMUM_PLAYERS:
			self.error_text.text = 'Two or more players are required'
		else:
			self.add_command(NetworkCommand('network_start_game', status='pending'))

	def network_start_game_handler(self, command):
		if command.status == 'not_enough_players':
			self.error_text.text = 'Two or more players are required'
		else:
			self.set_state(ClientSetupPlayerOrderState(self.set_state, self.add_command, self.player_name, self.game_name, self.host))
