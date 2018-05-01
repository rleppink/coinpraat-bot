import requests


def handler(incoming_queue, outgoing_queue):
    while True:
        update = longpoll_updates()

        incoming_queue.put("New message!")


def longpoll_updates():
    def valid_update(update_check):
        return \
            update_check is not None and
            update_check["ok"] is True and
            update_check["result"] is not []

    def get_update():
        requests.post(
            arbotrator.get_bot_url() + "getUpdates",
            data={"offset": update_id, "limit": 1, "timeout": 30})


    update = None
    while update is None:
        update = get_update()
        if not valid_update(update):
            update = None

    return update
