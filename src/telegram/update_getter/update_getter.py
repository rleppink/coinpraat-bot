import requests




def get_next_update():
    updates = _get_update_response()
    print(updates.json())
    print(_any_valid_updates(updates))


def _get_update_response(update_offset):
    # TODO: Set in config
    data = {"timeout": 30}

    if update_offset > 0:
        data["offset"] = update_offset

    # TODO: Replace URL
    return requests.post(
       "https://api.telegram.org/bot481981869:AAG9VBdLMMJLYGwZSSzkMlOdF0l-KxGtzL0/getUpdates",
        data={"timeout": 30})


def _any_valid_updates(update_response):
    return \
        update_response.status_code is 200 and \
        update_response.json() is not None and \
        update_response.json()["ok"] is True and \
        update_response.json()["result"] is not []


if __name__ == "__main__":
    get_next_update()
