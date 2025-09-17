from src.models import Command


class SubscribeCommand(Command):
    def execute(self, client_handler, args):
        if not args:
            client_handler.send({"error": "SUB requires topic"})
            return
        topic = args[0]
        client_handler.server.topic_manager.add_subscriber(topic, client_handler)
        client_handler.send({"status": f"Subscribed to {topic}"})
