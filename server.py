from config import CONFIG
from lattice2d.config import Config
from src.server.server_core import ServerCore

Config(CONFIG)
server = ServerCore()
server.run()