from config import CONFIG
from src.server.server_core import ServerCore

server = ServerCore(CONFIG)
server.run()