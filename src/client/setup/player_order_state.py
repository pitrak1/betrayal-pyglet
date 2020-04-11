import pyglet
from src.client.setup import character_selection_state
from src.client.common import button, label, state
from src.common import constants, command

class PlayerOrderState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, game_name, host, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.players = []
		self.redraw()
		self.add_command(command.Command('network_get_player_order', { 'status': 'pending' }))
		self.waiting = False

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(2)]
			self.elements = {
				'title': label.Label(
					text='Welcome to Betrayal Online',
					font_size=25,
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y + 200,
					anchor_x='center',
					anchor_y='center',
					align='center',
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'text1': label.Label(
					text='Turn order will be randomly determined', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y + 100, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'text2': label.Label(
					text='First player in the order will play first.', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y + 60, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'text3': label.Label(
					text='Last player in the order will choose their character first.', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y + 40, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'text4': label.Label(
					text='The player order is:', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y - 40, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				),
				'continue_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y - 140, 
					unit_width=12, 
					unit_height=3, 
					text='Continue', 
					on_click=self.continue_,
					batch=self.batch,
					area_group=self.groups[0],
					text_group=self.groups[1]
				),
				'waiting_text': label.Label(
					text='', 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y - 200, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				)
			}

			if len(self.players) > 0:
				player_text = ''
				for player in self.players:
					player_text += player
					player_text += ', '
				self.elements['players_text'] = label.Label(
					text=player_text[:-2], 
					x=constants.WINDOW_CENTER_X - 220, 
					y=constants.WINDOW_CENTER_Y - 60, 
					anchor_x='left', 
					anchor_y='center', 
					align='left', 
					font_size=15, 
					color=(255, 255, 255, 255),
					batch=self.batch,
					group=self.groups[0]
				)

	def set_player_order(self, players):
		self.players = players
		self.redraw()

	def continue_(self):
		if not self.waiting:
			self.waiting = True
			self.elements['waiting_text'].text = 'Waiting for other players...'
			self.add_command(command.Command('network_confirm_player_order', { 'status': 'pending' }))

	def next(self):
		self.set_state(character_selection_state.CharacterSelectionState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			self.game_name,
			self.host,
			testing=self.testing
		))
