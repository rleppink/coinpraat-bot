import time

import requests

from . import utilities


def get_workable_update(config, update_id):
    while True:
        update = _request_update_forever(config, update_id)
        update_json = update.json()

        if update_json is None \
        or update_json["ok"] is False \
        or update_json["result"] == []:
            continue

        return update_json["result"][0]


def _request_update_forever(config, update_id):
    """ Keep requesting an update until a valid one comes through. """
    request_num = 0
    while True:
        update = _request_update(config, update_id)

        if update is not None:
            return update

        request_num += 1
        time.sleep(request_num % 60)


def _request_update(config, update_id):
    """ Request an update, returns None if no valid update is given. """
    try:
        response = requests.post(
            utilities.telegram_bot_url(config) + "getUpdates",
            data={
                "timeout": config.api_timeout,
                "offset": update_id
            },
            timeout=config.api_timeout)

        if response is None \
        or response.status_code is not 200:
            return None

        return response
    except requests.exceptions.RequestException:
        return None
