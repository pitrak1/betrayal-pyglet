from src.server import server as server_module

server = server_module.Server()

if __name__ == "__main__":
	server.run()
