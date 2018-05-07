import multiprocessing
import types
import yaml

import coinmarketcap
import telegram


def main():
    config = read_config()

    telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    multiprocessing.Process(
        target=telegram.incoming.handler,
        args=(
            telegram_outgoing_queue,
            config,
        )).start()

    multiprocessing.Process(
        target=coinmarketcap.all_time_high.handler,
        args=(
            config,
            telegram_outgoing_queue,
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
