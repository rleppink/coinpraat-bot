import json


def handler(outgoing_queue):
    print("[OUT-] Started Telegram outgoing handler...")
    while True:
        message = outgoing_queue.get()
        print("[OUT-] Popped a message off the queue")
        print(json.dumps(message, indent=2))
