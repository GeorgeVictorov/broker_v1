from src.models import Command


class PublishCommand(Command):
    def execute(self, client_handler, args):
        if len(args) < 2:
            client_handler.send({"error": "PUB requires topic and message"})
            return
        topic = args[0]
        message = " ".join(args[1:])
        client_handler.server.topic_manager.publish(topic, message)
