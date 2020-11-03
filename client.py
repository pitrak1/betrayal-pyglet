from lattice2d.client import ClientCore
from config import CONFIG
from lattice2d.config import Config

Config(CONFIG)
c = ClientCore()
c.run()