import humanize
import requests

import arbotrator
import litebit_checker
import my_utils
import ticker
import total_marketcap


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


def longpoll_updates(update_id):
    update = \
        requests.post(
            arbotrator.get_bot_url() + "getUpdates",
            data={"offset": update_id, "limit": 1, "timeout": 30}).json()

    return update


def handle_update(update):
    if (update["ok"] is False) or \
       (update["result"] == []):
        return None

    result = update["result"][0]
    write_last_update_id(result["update_id"])

    if "message" not in result:
        # Something unknown is doing we don't know what.
        # That is what our knowledge amounts to.
        return

    if str(result["message"]["chat"]["id"]) != arbotrator.get_chat_id():
        # Ignore other chats
        return ""

    if "edited_message" in result:
        # Ain't nobody got time for that
        return ""

    message_text = \
        result["message"]["text"] \
        .encode("ascii", "ignore") \
        .decode("ascii")

    if message_text.startswith("/prijs"):
        handle_price(result)
    elif message_text.startswith("/check"):
        handle_check(result)
    elif message_text.startswith("/markt"):
        handle_market()

    return ""


def determine_coin_id(message_text):
    return "-".join(message_text.split(" ")[1:]).lower()


def nonermalize(ticker_result, key):
    if ticker_result[key] is None:
        return "Onbekend"

    return humanize.intword(int(float(ticker_result[key])))


def handle_price(update_result):
    coin_id = determine_coin_id(update_result["message"]["text"])

    # This try can be removed once the server has a newer version of Python
    try:
        ticker_result = ticker.get_ticker_result(coin_id)
    except UnicodeEncodeError:
        return

    if ticker_result is None:
        arbotrator.send_message(
            "Sorry, ik kan geen coin vinden met de naam \"{}\""
            .format(" ".join(update_result["message"]["text"].split(" ")[1:])))
        return

    mcap = nonermalize(ticker_result, "market_cap_usd")
    if mcap is not "Onbekend":
        mcap = "$" + mcap

    message = \
        """
📈 *{}* 📉

*$*{} | *€*{} | *B*{}
*1u* {}% | *24u* {}% | *7d* {}%

Market cap *USD*: {}
Voorraad: {} / {}

_Prijs van {}_
https://coinmarketcap.com/currencies/{}
        """.format(ticker_result["name"],
                   ticker_result["price_usd"],
                   ticker_result["price_eur"],
                   ticker_result["price_btc"],
                   ticker_result["percent_change_1h"],
                   ticker_result["percent_change_24h"],
                   ticker_result["percent_change_7d"],
                   mcap,
                   nonermalize(ticker_result, "available_supply"),
                   nonermalize(ticker_result, "total_supply"),
                   my_utils
                   .convert_unix_timestamp(
                        int(ticker_result["last_updated"])),
                   ticker_result["id"])

    arbotrator.send_message(message)


def handle_check(update_result):
    coin_id = " ".join(update_result["message"]["text"].lower().split(" ")[1:])
    litebit_checker.add_check(coin_id)


def handle_market():
    market_differences = total_marketcap.get_market_differences()

    arbotrator.send_message(
        """
📈 *Totale markt* 📉

*1u*: {:+0.2f}% | *24u*: {:+0.2f}% | *7d*: {:+0.2f}%
https://coinmarketcap.com/charts/
        """.format(market_differences[0],
                   market_differences[1],
                   market_differences[2]))


if __name__ == "__main__":
    update = longpoll_updates(-1)
    while True:
        handle_update(update)
        update_id = int(get_last_update_id()) + 1
        update = longpoll_updates(update_id)
