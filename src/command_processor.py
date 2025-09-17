from src.commands import (CREATE, EXIT, PUB, SUB, CreateTopicCommand,
                          PublishCommand, SubscribeCommand)


class CommandProcessor:
    def __init__(self):
        self.commands = {
            CREATE: CreateTopicCommand,
            PUB: PublishCommand,
            SUB: SubscribeCommand,
            EXIT: None
        }

    def handle(self, client_handler, action, args):
        if action.upper() == EXIT:
            client_handler.send({"system": "bye"})
            client_handler.conn.close()
            return

        cmd = self.commands.get(action.upper())
        if cmd:
            cmd.execute(client_handler, args)
        else:
            client_handler.send({"error": f"Unknown command {action}"})
