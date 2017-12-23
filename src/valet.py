import requests
import time

import arbotrator
import my_utils
import ticker


def get_update_id_file():
    return "../data/last_update_id"


def get_last_update_id():
    try:
        with open(get_update_id_file(), "r") as last_update_id_file:
            return last_update_id_file.read().strip()
    except FileNotFoundError:
        return -1


def write_last_update_id(last_update_id):
    with open(get_update_id_file(), "w") as last_update_id_file:
        last_update_id_file.write(str(last_update_id))


def longpoll_updates():
    update_id = int(get_last_update_id()) + 1
    update = \
        requests.post(
            arbotrator.get_bot_url() + "getUpdates",
            data = { "offset": update_id, "limit": 1, "timeout": 30 }).json()

    return update


def handle_update(update):
    if (update["ok"] is False) or \
       (update["result"] == []):
        return None

    result = update["result"][0]
    write_last_update_id(result["update_id"])

    if result["message"]["text"].startswith("/prijs"):
        handle_price(result)

    return ""


def determine_coin_id(message_text):
    return "-".join(message_text.split(" ")[1:]).lower()


def handle_price(update_result):
    coin_id = determine_coin_id(update_result["message"]["text"])
    ticker_result = ticker.get_ticker_result(coin_id)

    if ticker_result is None:
        arbotrator.send_message(
            "Sorry, ik kan geen coin vinden met de naam \"{}\"" \
            .format(" ".join(update_result["message"]["text"].split(" ")[1:])))
        return

    message = \
        """
📈 *{}* 📉

Huidige prijs *USD*: ${}
Huidige prijs *EUR*: €{}
Huidige prijs *BTC*: B{}

Verandering *1u*: {}%
Verandering *24u*: {}%
Verandering *7d*: {}%

_Prijs van {}_
        """.format(ticker_result["name"],
                   ticker_result["price_usd"],
                   ticker_result["price_eur"],
                   ticker_result["price_btc"],
                   ticker_result["percent_change_1h"],
                   ticker_result["percent_change_24h"],
                   ticker_result["percent_change_7d"],
                   my_utils \
                   .convert_unix_timestamp(
                        int(ticker_result["last_updated"])))

    arbotrator.send_message(message)


if __name__ == "__main__":
    while True:
        update = longpoll_updates()
        handle_update(update)
