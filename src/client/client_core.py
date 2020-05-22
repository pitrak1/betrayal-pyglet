from lattice2d.full.full_client import FullClient, FullClientNetwork
from src.client.client_menu_states import ClientMenuSplashState

class ClientCore(FullClient):
	def __init__(self):
		super().__init__()
		self.set_state(ClientMenuSplashState(self.set_state, self.add_command))
