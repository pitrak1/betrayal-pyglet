from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.area import Area
from lattice2d.client.components.button import Button
from lattice2d.client.components.label import Label
from constants import WINDOW_CENTER

class SplashState(ClientState):
	def redraw(self):
		self.children = [
			Background(
				asset_key='menu_background',
				batch=self.renderer.get_batch(), 
				group=self.renderer.get_group(0)
			),
			Area(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
				unit_dimensions=(10, 15), 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] + 50),
				unit_dimensions=(12, 3),
				text='Begin', 
				on_click=self.begin,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Label(
				text='Betrayal Online',
				font_size=25,
				x=WINDOW_CENTER[0], 
				y=WINDOW_CENTER[1] + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			)
		]

	def begin(self):
		self.to_create_player_state()