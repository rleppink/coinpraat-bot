import multiprocessing

import shared
import telegram


def main():
    config = shared.config.Config()

    telegram_incoming_queue = multiprocessing.Queue(config.queue_size)
    telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    telegram_incoming_handler = \
            multiprocessing.Process(
                    target = telegram.incoming.handler,
                    args = (telegram_incoming_queue, config,))

    telegram_outgoing_handler = \
            multiprocessing.Process(
                    target = telegram.outgoing.handler,
                    args = (telegram_outgoing_queue,))

    telegram_incoming_handler.start()
    telegram_outgoing_handler.start()

    multiprocessing.Process(
        target=dummy_handler,
        args=(
            telegram_incoming_queue,
            telegram_outgoing_queue,
        )).start()



def dummy_handler(incoming_queue, outgoing_queue):
    print("[MAIN] Started dummy handler...")
    while True:
        message = incoming_queue.get()
        outgoing_queue.put(message)


if __name__ == "__main__":
    main()
