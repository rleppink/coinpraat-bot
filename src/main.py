import multiprocessing

import price_checker
import shared
import telegram


def main():
    config = shared.config.Config()

    price_check_queue \
    = litebit_check_queue \
    = market_cap_check_queue \
    = telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    multiprocessing.Process(
        target = telegram.incoming.handler,
        args = (
            price_check_queue,
            config,
        )).start()

    multiprocessing.Process(
        target=price_checker.price_checker.handler,
        args=(
            price_check_queue,
            telegram_outgoing_queue,
            config,
        )).start()

    multiprocessing.Process(
        target = telegram.outgoing.handler,
        args = (
            telegram_outgoing_queue,
        )).start()


# Dummy process
def queue_glue(in_queue, out_queue):
    print("[MAIN] Started queue glue...")
    while True:
        message = in_queue.get()
        out_queue.put(message)


if __name__ == "__main__":
    main()
