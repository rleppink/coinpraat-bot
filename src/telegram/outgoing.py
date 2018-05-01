

def handler(outgoing_queue):
    while True:
        message = outgoing_queue.get()
        print(message)
