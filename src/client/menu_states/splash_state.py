from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, Label
from constants import WINDOW_CENTER

class SplashState(ClientState):
	def __init__(self, state_machine, custom_data = {}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(10, 15)
		))
		self.register_component('begin_button', 'ui', Button(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1] + 50),
			unit_dimensions=(12, 3),
			text='Begin',
			on_click=self.begin
		))
		self.register_component('title', 'ui', Label(
			text='Betrayal Online',
			font_size=25,
			x=WINDOW_CENTER[0],
			y=WINDOW_CENTER[1] + 150,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255),
			align='center'
		))

	def begin(self):
		self.to_create_player_state()