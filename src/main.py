import multiprocessing

import shared
import telegram


def main():
    config = shared.config.Config()

    price_check_queue = multiprocessing.Queue(config.queue_size)
    telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    multiprocessing.Process(
        target = telegram.incoming.handler,
        args = (
            price_check_queue,
            config,
        )).start()

    multiprocessing.Process(
        target = telegram.outgoing.handler,
        args = (
            telegram_outgoing_queue,
        )).start()

    multiprocessing.Process(
        target=queue_glue,
        args=(
            price_check_queue,
            telegram_outgoing_queue,
        )).start()



def queue_glue(in_queue, out_queue):
    print("[MAIN] Started queue glue...")
    while True:
        message = in_queue.get()
        out_queue.put(message)


if __name__ == "__main__":
    main()
