import sys
from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, TextBox, Label
from src.client.components import GameListing, GamePlayer
from lattice2d.utilities import get_page_info
from lattice2d.command import Command
from constants import Constants

class SplashState(ClientState):
	def __init__(self, state_machine, custom_data = {}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(10, 15)
		))
		self.register_component('begin_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y + 50),
			unit_dimensions=(12, 3),
			text='Begin',
			on_click=self.begin
		))
		self.register_component('title', 'ui', Label(
			text='Betrayal Online',
			font_size=25,
			x=Constants.window_center_x,
			y=Constants.window_center_y + 150,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255),
			align='center'
		))

	def begin(self):
		self.to_create_player_state()

class CreatePlayerState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(10, 15)
		))
		self.register_component('name_input', 'environment', TextBox(
			position=(Constants.window_center_x - 120, Constants.window_center_y + 50),
			unit_width=8,
			label_text='Player Name',
			max_length=23
		))
		self.register_component('continue_button', 'environment', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 50),
			unit_dimensions=(12, 3),
			text='Continue',
			on_click=self.continue_
		))
		self.register_component('exit_button', 'environment', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 110),
			unit_dimensions=(12, 3),
			text='Exit',
			on_click=self.exit
		))
		self.register_component('title', 'environment', Label(
			text='Betrayal Online',
			font_size=25,
			x=Constants.window_center_x,
			y=Constants.window_center_y + 150,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))

	def exit(self):
		sys.exit()

	def continue_(self):
		player_name = self.get_component('name_input').get_text()
		if len(player_name) < 6:
			self.get_component('name_input').set_error_text('must be >5 characters')
		else:
			self.add_command(Command('create_player', { 'player_name': player_name }, 'pending'))

	def create_player_handler(self, command):
		if command.status == 'name_too_short':
			self.get_component('name_input').set_error_text('must be >5 characters')
		elif command.status == 'name_too_long':
			self.get_component('name_input').set_error_text('must be <26 characters')
		elif command.status == 'invalid_name':
			self.get_component('name_input').set_error_text('name is taken')
		elif command.status == 'success':
			self.to_main_menu_state({ 'player_name': command.data['player_name'] })


class MainMenuState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(10, 15)
		))
		self.register_component('create_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y + 50),
			unit_dimensions=(12, 3),
			text='Create Game',
			on_click=self.create_game
		))
		self.register_component('join_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 30),
			unit_dimensions=(12, 3),
			text='Join Game',
			on_click=self.join_game
		))
		self.register_component('exit_button', 'ui', Button(
			position=(Constants.window_center_x, Constants.window_center_y - 110),
			unit_dimensions=(12, 3),
			text='Exit',
			on_click=self.exit
		))
		self.register_component('title', 'ui', Label(
			text='Betrayal Online',
			font_size=25,
			x=Constants.window_center_x,
			y=Constants.window_center_y + 150,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))

	def exit(self):
		self.add_command(Command('logout', status='pending'))

	def logout_handler(self, command):
		if command.status == 'success':
			sys.exit()

	def create_game(self):
		self.to_create_game_state(self.custom_data)

	def join_game(self):
		self.to_join_game_state(self.custom_data)


class CreateGameState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(20, 15)
		))
		self.register_component('name_input', 'ui', TextBox(
		    position=(Constants.window_center_x - 200, Constants.window_center_y + 50), 
			unit_width=13, 
			label_text='Game Name',
			max_length=40
		))
		self.register_component('back_button', 'ui', Button(
			position=(Constants.window_center_x - 150, Constants.window_center_y - 100),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.back
		))
		self.register_component('create_button', 'ui', Button(
			position=(Constants.window_center_x + 150, Constants.window_center_y - 100),
			unit_dimensions=(12, 3),
			text='Create',
			on_click=self.create
		))
		self.register_component('title', 'ui', Label(
			text='Create Game',
			x=Constants.window_center_x,
			y=Constants.window_center_y + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			font_size=25,
			color=(0, 0, 0, 255)
		))
		
	def back(self):
		self.to_main_menu_state(self.custom_data)

	def create(self):
		game_name = self.get_component('name_input').get_text()
		if len(game_name) < 6:
			self.get_component('name_input').set_error_text('must be >5 characters')
		else:
			self.add_command(Command('create_game', { 'game_name': game_name }, 'pending'))

	def create_game_handler(self, command):
		if command.status == 'invalid_name':
			self.get_component('name_input').set_error_text('name is taken')
		elif command.status == 'name_too_short':
			self.get_component('name_input').set_error_text('must be >5 characters')
		elif command.status == 'name_too_long':
			self.get_component('name_input').set_error_text('must be <41 characters')
		else:
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': True })
			self.to_lobby_state(self.custom_data)


class GameListState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		self.__current_page = 0
		self.__available_games = []
		self.__available_games_count = 0
		super().__init__(state_machine, custom_data)
		self.add_command(Command('get_games', status='pending'))
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(20, 15)
		))
		self.register_component('back_button', 'ui', Button(
			position=(Constants.window_center_x - 150, Constants.window_center_y - 185),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.back
		))
		self.register_component('refresh', 'ui', Button(
			position=(Constants.window_center_x + 150, Constants.window_center_y - 185),
			unit_dimensions=(12, 3),
			text='Refresh',
			on_click=self.refresh
		))
		self.register_component('error_label', 'ui', Label(
			text='',
			font_size=15,
			x=Constants.window_center_x + 150,
			y=Constants.window_center_y - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255)
		))
		self.register_component('title', 'ui', Label(
			text='Games',
			font_size=25,
			x=Constants.window_center_x,
			y=Constants.window_center_y + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))

	def __redraw(self):
		if self.__available_games_count > 0:
			for count in range(0, Constants.game_list_page_size):
				self.conditionally_remove_component(f'game_{count}')
				self.conditionally_remove_component('down_button')
				self.conditionally_remove_component('up_button')

			min_, max_, down, up = get_page_info(
				self.__current_page, 
				Constants.game_list_page_size, 
				self.__available_games_count
			)

			count = 0
			for game in self.__available_games[min_:max_]:
				if game == '': break
				self.register_component(f'game_{count}', 'ui', GameListing(
					name=game[0], 
					players=game[1], 
					position=(Constants.window_center_x - 200, Constants.window_center_y + 120 - 40 * (count % Constants.game_list_page_size)), 
					on_click=lambda : self.join(game[0], int(game[1]))
				))
				count += 1

			if down:
				self.register_component('down_button', 'ui', Button(
					position=(Constants.window_center_x + 250, Constants.window_center_y - 50), 
					unit_dimensions=(2, 3), 
					text='Down', 
					on_click=self.go_forward_page
				))

			if up:
				self.register_component('up_button', 'ui', Button(
					position=(Constants.window_center_x + 250, Constants.window_center_y + 50),
					unit_dimensions=(2, 3),
					text='Up',
					on_click=self.go_back_page
				))

	def get_games_handler(self, command):
		if command.status == 'success':
			self.__current_page = 0
			self.__available_games = command.data['games']
			self.__available_games_count = len(command.data['games'])
			self.__redraw()

	def go_forward_page(self):
		self.__current_page += 1
		self.__redraw()

	def go_back_page(self):
		self.__current_page -= 1
		self.__redraw()

	def refresh(self):
		self.add_command(Command('get_games', status='pending'))

	def back(self):
		self.to_main_menu_state(self.custom_data)

	def join(self, game, number_of_players):
		if number_of_players >= Constants.max_players_per_game:
			self.get_component('error_label').text = 'Game is full'
		else:
			self.add_command(Command('join_game', { 'game_name': game }, 'pending'))

	def join_game_handler(self, command):
		if command.status == 'game_full':
			self.get_component('error_label').text = 'Game is full'
		elif command.status == 'success':
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': False })
			self.to_lobby_state(self.custom_data)


class LobbyState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		self.players = []
		super().__init__(state_machine, custom_data)
		self.add_command(Command('broadcast_players_in_game', status='pending'))
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(Constants.window_center_x, Constants.window_center_y),
			unit_dimensions=(20, 15)
		))
		self.register_component('back_button', 'ui', Button(
			position=(Constants.window_center_x - 150, Constants.window_center_y - 185),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.leave_game
		))
		self.register_component('title', 'ui', Label(
			text=self.custom_data['game_name'],
			font_size=25,
			x=Constants.window_center_x,
			y=Constants.window_center_y + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('error_label', 'ui', Label(
			text='',
			font_size=15,
			x=Constants.window_center_x + 150,
			y=Constants.window_center_y - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255)
		))
		if self.custom_data['host']:
			self.register_component('start_button', 'ui', Button(
				position=(Constants.window_center_x + 150, Constants.window_center_y - 185),
				unit_dimensions=(12, 3),
				text='Start',
				on_click=self.start_game
			))
		self.__draw_players()

	def __draw_players(self):
		for count in range(0, 10):
			self.conditionally_remove_component(f'player_{count}')

		count = 0
		for player in self.players:
			self.register_component(f'player_{count}', 'ui', GamePlayer(
				name=player[0], 
				host=player[1], 
				position=(Constants.window_center_x - 200, Constants.window_center_y + 120 - 80 * count)
			))
			count += 1

	def broadcast_players_in_game_handler(self, command):
		if command.status == 'success':
			self.players = command.data['players']
			self.__draw_players()

	def leave_game(self):
		self.add_command(Command('leave_game', status='pending'))

	def leave_game_handler(self, command):
		if command.status == 'success':
			self.to_main_menu_state(self.custom_data)

	def start_game(self):
		if len(self.players) < Constants.min_players_per_game:
			self.get_component('error_label').text = 'Two or more players are required'
		else:
			self.add_command(Command('start_game', status='pending'))

	def start_game_handler(self, command):
		if command.status == 'not_enough_players':
			self.get_component('error_label').text = 'Two or more players are required'
		else:
			self.to_player_order_state(self.custom_data)

