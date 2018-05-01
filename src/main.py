import multiprocessing

import all_time_high_tracker
import telegram_handler


QUEUE_SIZE = 10


def main():
    telegram_incoming_queue = multiprocessing.Queue(QUEUE_SIZE)
    telegram_outgoing_queue = multiprocessing.Queue(QUEUE_SIZE)

    telegram_incoming_handler = \
            multiprocessing.Process(target = telegram_handler.incoming, args = (telegram_incoming,))

    telegram_outgoing_handler = \
            multiprocessing.Process(target = telegram_handler.outgoing, args = (telegram_outgoing,))

    all_time_high_tracker_handler = \
            multiprocessing.Process(target = telegram_handler.outgoing, args = (telegram_outgoing,))

    telegram_incoming_handler.start()
    telegram_outgoing_handler.start()
    all_time_high_tracker_handler.start()


if __name__ == "__main__"
    main()
