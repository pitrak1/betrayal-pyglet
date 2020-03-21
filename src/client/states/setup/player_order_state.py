import pyglet
from src.client.states.setup import character_selection_state
from src.client.states import state
from src.client.world.common import button, label 
from src.shared import constants, command

class PlayerOrderState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_player_order', { 'status': 'pending' }))
		self.__waiting = False

	def __create_base_elements(self):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(2)]

		return [
			label.Label(
				text='Welcome to Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			),
			label.Label(
				text='Turn order will be randomly determined', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 100, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			),
			label.Label(
				text='First player in the order will play first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 60, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			),
			label.Label(
				text='Last player in the order will choose their character first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 40, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			),
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y - 140, 
				unit_width=12, 
				unit_height=3, 
				text='Continue', 
				on_click=self.__confirm_order,
				batch=self._batch,
				area_group=self.__groups[0],
				text_group=self.__groups[1]
			)
		]

	def set_player_order(self, players):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(2)]
		self._elements = self.__create_base_elements()
		self._elements.append(label.Label(
			text='The player order is:', 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 40, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255),
			batch=self._batch,
			group=self.__groups[0]
		))
		player_text = ''
		for player in players:
			player_text += player
			player_text += ', '
		self._elements.append(label.Label(
			text=player_text[:-2], 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 60, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255),
			batch=self._batch,
			group=self.__groups[0]
		))

	def __confirm_order(self):
		if not self.__waiting:
			self.__waiting = True
			self._elements.append(label.Label(
				text='Waiting for other players...', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 200, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255),
				batch=self._batch,
				group=self.__groups[0]
			))
			self._add_command(command.Command('network_confirm_player_order', { 'status': 'pending' }))

	def next(self):
		self._set_state(character_selection_state.CharacterSelectionState(
			self._data,
			self._set_state, 
			self._add_command
		))
