import requests


def get_next_update():
    updates = _get_all_updates()
    print(updates)
    print(_any_valid_updates(updates))

def _get_all_updates():
    requests.post(
       "https://api.telegram.org/bot481981869:AAG9VBdLMMJLYGwZSSzkMlOdF0l-KxGtzL0/getUpdates",
        data={"timeout": 30})

def _any_valid_updates(update):
    return \
        update is not None and
        update["ok"] is True and
        update["result"] is not []


if __name__ == "__main__":
    get_next_update()
