from src.commands import (CREATE, PUB, SUB, CreateTopicCommand, PublishCommand,
                          SubscribeCommand)


class CommandProcessor:
    def __init__(self):
        self.commands = {
            CREATE: CreateTopicCommand,
            PUB: PublishCommand,
            SUB: SubscribeCommand,
        }

    def handle(self, client_handler, action, args):
        cmd = self.commands.get(action.upper())
        if cmd:
            cmd.execute(client_handler, args)
        else:
            client_handler.send({"error": f"Unknown command {action}"})
