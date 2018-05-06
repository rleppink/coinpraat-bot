import multiprocessing
import types
import yaml

import coinmarketcap
import telegram


def main():
    config = read_config()

    price_check_queue = multiprocessing.Queue(config.queue_size)
    market_cap_check_queue = multiprocessing.Queue(config.queue_size)
    litebit_check_queue = multiprocessing.Queue(config.queue_size)
    telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    multiprocessing.Process(
        target=telegram.incoming.handler,
        args=(
            price_check_queue,
            market_cap_check_queue,
            litebit_check_queue,
            telegram_outgoing_queue,
            config,
        )).start()

    multiprocessing.Process(
        target=coinmarketcap.price_checker.handler,
        args=(
            price_check_queue,
            telegram_outgoing_queue,
            config,
        )).start()

    multiprocessing.Process(
        target=telegram.outgoing.handler,
        args=(telegram_outgoing_queue, config)).start()


def queue_glue(in_queue, out_queue):
    # Just a dummy process for testing purposes
    print("[MAIN] Started queue glue...")
    while True:
        message = in_queue.get()
        out_queue.put(message)


def read_config():
    config_path = "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        return types.SimpleNamespace(**config)


if __name__ == "__main__":
    main()