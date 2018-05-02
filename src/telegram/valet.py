import humanize
import requests

import arbotrator
import litebit_checker
import my_utils
import ticker
import total_marketcap


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


def handle_check(update_result):
    coin_id = " ".join(update_result["message"]["text"].lower().split(" ")[1:])
    litebit_checker.add_check(coin_id)


def handle_market():
    market_differences = total_marketcap.get_market_differences()

    if market_differences is None:
        return

    arbotrator.send_message("""
📈 *Totale markt* 📉

*1u*: {:+0.2f}% | *24u*: {:+0.2f}% | *7d*: {:+0.2f}%
Market cap *USD*: ${}

https://coinmarketcap.com/charts/
        """.format(market_differences[0], market_differences[1],
                   market_differences[2],
                   humanize.intword(market_differences[3])))


if __name__ == "__main__":
    update = longpoll_updates(-1)
    while True:
        if update is not None:
            handle_update(update)
            update_id = int(get_last_update_id()) + 1

        update = longpoll_updates(update_id)
