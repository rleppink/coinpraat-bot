import os

import munch

from . import update_getter


def handler(config, incoming_message_queue):
    print("[IN--] Started Telegram incoming handler...")

    while True:
        next_update_id = _get_next_update_id(config)

        raw_update = update_getter.get_workable_update(config, next_update_id)
        update = munch.Munch.fromDict(raw_update)

        _write_last_update_id(config, update.update_id)

        incoming_message_queue.put(update.message)


def _get_next_update_id(config):
    last_update_id = _get_last_update_id(config)

    if last_update_id is None:
        return -1
    else:
        return int(last_update_id) + 1


def _get_last_update_id(config):
    try:
        with open(_last_update_id_path(config), "r") as last_update_id_file:
            return last_update_id_file.read().strip()
    except FileNotFoundError:
        return None


def _write_last_update_id(config, last_update_id):
    os.makedirs(_last_update_id_dir(config), exist_ok=True)

    with open(_last_update_id_path(config), "w") as last_update_id_file:
        last_update_id_file.write(str(last_update_id))


def _last_update_id_path(config):
    return os.path.join(_last_update_id_dir(config), "last_update_id")


def _last_update_id_dir(config):
    return os.path.join(config.data_path, "telegram")
