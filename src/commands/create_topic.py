from src.models import Command


class CreateTopicCommand(Command):
    def execute(self, client_handler, args):
        if not args:
            client_handler.send({"error": "CREATE requires topic"})
            return
        topic = args[0]
        tm = client_handler.server.topic_manager
        with tm.lock:
            if topic not in tm.topics:
                tm.topics[topic] = []
                client_handler.send({"status": f"Topic {topic} created"})
            else:
                client_handler.send({"status": f"Topic {topic} already exists"})
