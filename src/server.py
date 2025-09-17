import socket
import threading
import sys
from topic_manager import TopicManager
from command_processor import CommandProcessor
from client_handler import ClientHandler

HOST = "127.0.0.1"
PORT = 65432


class BrokerServer:
    def __init__(self, host, port):
        self.topic_manager = TopicManager()
        self.command_processor = CommandProcessor()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.client_handlers = []
        self.running = True

    def start(self):
        print(f"Broker listening on {HOST}:{PORT}")
        try:
            while self.running:
                conn, addr = self.server.accept()
                handler = ClientHandler(conn, addr, self)
                self.client_handlers.append(handler)
                threading.Thread(target=handler.handle, daemon=True).start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down...")
            self.shutdown()

    def shutdown(self):
        for handler in self.client_handlers:
            try:
                handler.send({"system": "server_shutdown"})
                handler.conn.close()
            except:  # noqa
                pass

        self.running = False
        self.server.close()
        print("[!] Server stopped")
        sys.exit(0)


if __name__ == "__main__":
    server = BrokerServer(HOST, PORT)
    server.start()
