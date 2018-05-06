import os

import telegram.update_getter
from shared.messages import OutgoingMessage, MessageType


def handler(price_check_queue, market_cap_queue, litebit_queue,
            telegram_outgoing_queue, config):
    print("[IN--] Started Telegram incoming handler...")

    while True:
        next_update_id = get_next_update_id(config)

        update = telegram.update_getter.get_workable_update(
            config, next_update_id)

        write_last_update_id(config, update["update_id"])

        bot_command = try_get_bot_command(update)
        if bot_command is None:
            continue

        print("[IN--] " + str(bot_command))
        if bot_command[0] == "/prijs":
            price_check_queue.put(bot_command)
        elif bot_command[0] == "/markt":
            market_cap_queue.put(bot_command)
        elif bot_command[0] == "/check":
            litebit_queue.put(bot_command)
        elif bot_command[0] == "/testing":
            telegram_outgoing_queue.put(
                OutgoingMessage(MessageType.TYPING, None,
                                update["message"]["chat"]["id"], None))
        else:
            telegram_outgoing_queue.put(
                OutgoingMessage(MessageType.TEXT,
                                "Sorry, daar kan ik niks mee.",
                                update["message"]["chat"]["id"],
                                update["message"]["message_id"]))


def try_get_bot_command(update):
    """
    Attempt to get a command from the given message. Return None if not
    succesful.
    """
    try:
        entity = update["message"]["entities"][0]
        if entity["type"] != "bot_command":
            return None

        return update["message"]["text"].split(' ', 1)
    except KeyError:
        # No message, not a bot command, etc. Not something we can or should
        # handle, so just ignore
        return None


def get_next_update_id(config):
    last_update_id = get_last_update_id(config)

    if last_update_id is None:
        return -1
    else:
        return int(last_update_id) + 1


def get_last_update_id(config):
    try:
        with open(last_update_id_path(config), "r") as last_update_id_file:
            return last_update_id_file.read().strip()
    except FileNotFoundError:
        return None


def write_last_update_id(config, last_update_id):
    os.makedirs(last_update_id_dir(config), exist_ok=True)

    with open(last_update_id_path(config), "w") as last_update_id_file:
        last_update_id_file.write(str(last_update_id))


def last_update_id_path(config):
    return os.path.join(last_update_id_dir(config), "last_update_id")


def last_update_id_dir(config):
    return os.path.join(config.data_path, "telegram")
