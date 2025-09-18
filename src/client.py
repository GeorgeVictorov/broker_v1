import socket
import threading
import json
import sys
from src.commands import CREATE, EXIT, PUB, SUB

HOST = "127.0.0.1"
PORT = 65432


def recv_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[!] Disconnected from server")
                break
            try:
                msg = json.loads(data.decode())
                topic = msg.get("topic")
                payload = msg.get("message")
                status = msg.get("status")
                error = msg.get("error")

                if topic and payload:
                    print(f"\n[MSG] {topic}: {payload}")
                elif status:
                    print(f"\n[OK] {status}")
                elif error:
                    print(f"\n[ERR] {error}")
            except json.decoder.JSONDecodeError:
                print(f"\n[RAW] {data.decode()}")
        except OSError:
            break


def cmd_sub(sock, args):
    if len(args) < 1:
        print("Usage: SUB <topic>")
        return
    sock.sendall(json.dumps({"action": SUB, "topic": args[0]}).encode())


def cmd_pub(sock, args):
    if len(args) < 2:
        print("Usage: PUB <topic> <message>")
        return
    topic, message = args[0], " ".join(args[1:])
    sock.sendall(json.dumps({"action": PUB, "topic": topic, "message": message}).encode())


def cmd_create(sock, args):
    if len(args) < 1:
        print("Usage: CREATE <topic>")
        return
    sock.sendall(json.dumps({"action": CREATE, "topic": args[0]}).encode())


def cmd_exit(sock, args):
    print("[!] Client exit")
    sock.close()
    sys.exit(0)


COMMANDS = {
    SUB: cmd_sub,
    PUB: cmd_pub,
    CREATE: cmd_create,
    EXIT: cmd_exit,
}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("[!] Cannot connect to server")
        return

    print(f"[+] Connected to server")
    threading.Thread(target=recv_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            cmd_line = input("> ").strip()
            if not cmd_line:
                continue
            parts = cmd_line.split()
            action, args = parts[0].upper(), parts[1:]
            handler = COMMANDS.get(action)
            if handler:
                handler(sock, args)
            else:
                print("Commands:", ", ".join(COMMANDS.keys()))
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt: client stopped")
        sock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
