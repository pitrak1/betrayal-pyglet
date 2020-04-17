import pyglet
from src.client.game import client_game_state, client_player
from src.client.common import button, label, state
from src.common import constants, command

class CharacterOverviewState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, game_name, host, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.player_selections = []
		self.redraw()
		self.add_command(command.Command('network_get_character_selections', { 'status': 'pending' }))
		self.waiting = False

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(2)]
			self.elements = {
				'text1': label.Label(
					text='The players\' selected characters are:', 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_HEIGHT - 40, 
					anchor_x='center', 
					anchor_y='center', 
					align='center', 
					font_size=25, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'waiting_text': label.Label(
					text='', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y - 260, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'begin_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y - 200, 
					unit_width=12, 
					unit_height=3, 
					text='Begin', 
					on_click=self.confirm_characters,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1]
				)
			}

			if len(self.player_selections) > 0:
				count = 0
				for selection in self.player_selections:
					label_text = f'{selection[0]}: {selection[1]}'
					self.elements[f'player_{count}'] = label.Label(
						text=label_text, 
						x=constants.WINDOW_CENTER_X - 180, 
						y=constants.WINDOW_CENTER_Y + 130 - (40 * count), 
						anchor_x='left', 
						anchor_y='center', 
						align='left', 
						font_size=18, 
						color=(255, 255, 255, 255),
						batch=self.batch,
						group=self.groups[0]
					)
					count += 1


	def set_character_selections(self, selections):
		self.player_selections = selections
		self.redraw()

	def confirm_characters(self):
		if not self.waiting:
			self.waiting = True
			self.elements['waiting_text'].text = 'Waiting for other players...'
			self.add_command(command.Command('network_confirm_character_selections', { 'status': 'pending' }))

	def next(self):
		self.set_state(client_game_state.ClientGameState(
			self.asset_manager, 
			self.set_state, 
			self.add_command, 
			self.player_name,
			self.game_name,
			self.host,
			testing=self.testing
		))
