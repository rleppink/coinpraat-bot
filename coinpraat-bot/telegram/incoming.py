import json
import os

import requests

import telegram.update_getter


def handler(price_check_queue, config):
    print("[IN--] Started Telegram incoming handler...")

    while True:
        next_update_id = get_next_update_id(config)

        update = telegram.update_getter.get_workable_update(
            config, next_update_id)

        write_last_update_id(config, update["update_id"])

        # TODO: Use a less stringly typed, more strongly typed approach. json to namedtuples?

        if "message" not in update:
            continue

        message = update["message"]
        if "entities" not in message:
            continue

        entities = message["entities"]
        if entities == []:
            continue

        entity = entities[0]
        if entity["type"] != "bot_command":
            continue

        command = message["text"][entity["offset"]:entity["length"]]
        if command == "/prijs":
            price_check_queue.put(update)


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
    return config["data_path"] + "telegram/" + "last_update_id"


def last_update_id_dir(config):
    return config["data_path"] + "telegram/"
