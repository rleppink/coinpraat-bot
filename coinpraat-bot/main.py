""" CoinpraatBot main.

CoinpraatBot is a bot made to fulfill some tasks for a Telegram crypto group,
like:
 - Make price checks on CoinMarketCap
 - Alert on coins reaching an all-time-high
 - Give a total marketcap output
 - Check whether LiteBit has coins available
"""

import multiprocessing

import coinmarketcap
import message_handler
import shared
import telegram


def main():
    config = shared.utilities.read_config()
    telegram_incoming_queue = multiprocessing.Queue(config.queue_size)
    telegram_outgoing_queue = multiprocessing.Queue(config.queue_size)

    multiprocessing.Process(
        target=telegram.incoming.handler,
        args=(
            config,
            telegram_incoming_queue,
        )).start()

    multiprocessing.Process(
        target=message_handler.handler,
        args=(
            config,
            telegram_incoming_queue,
            telegram_outgoing_queue,
        )).start()
    '''
    multiprocessing.Process(
        target=coinmarketcap.track_ath.handler,
        args=(
            config,
            telegram_outgoing_queue,
        )).start()
    '''

    multiprocessing.Process(
        target=telegram.outgoing.handler,
        args=(config, telegram_outgoing_queue)).start()


def queue_glue(in_queue, out_queue):
    # Just a dummy process for testing purposes
    print("[MAIN] Started queue glue...")
    while True:
        message = in_queue.get()
        out_queue.put(message)


if __name__ == "__main__":
    main()
