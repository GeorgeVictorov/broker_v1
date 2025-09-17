import json

from src.commands import PUB


class ClientHandler:
    def __init__(self, conn, addr, server):
        self.conn = conn
        self.addr = addr
        self.server = server

    def handle(self):
        print(f"[+] Connected {self.addr}")

        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                try:
                    msg = json.loads(data.decode())
                except json.decoder.JSONDecodeError:
                    self.send({"error": "invalid json"})
                    continue

                action = msg.get("action")
                args = []
                if action.upper() == PUB:
                    args = [msg.get('topic'), msg.get('message')]
                else:
                    topic = msg.get('topic')
                    if topic:
                        args = [topic]

                self.server.command_processor.handle(self, action, args)
        except ConnectionResetError:
            pass
        finally:
            self.cleanup()
            self.conn.close()
            print(f"[-] Disconnected {self.addr}")

    def send(self, msg_dict):
        try:
            self.conn.sendall(json.dumps(msg_dict).encode())
        except:  # noqa
            pass

    def notify(self, topic, message):
        self.send({"topic": topic, "message": message})

    def cleanup(self):
        tm = self.server.topic_manager
        with tm.lock:
            for subs in tm.topics.values():
                if self in subs:
                    subs.remove(self)
