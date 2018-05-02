import json


def handler(price_check_queue, telegram_outgoing_queue, config):
    print("[PRCH] Starting price checker...")
    while True:
        price_check_update = price_check_queue.get()

        print("[PRCH] Got price check request: ")
        print(json.dumps(price_check_update, indent=2))

        message = price_check_update["message"]
        coin_id = "-".join(message["text"].split(" ")[1:]).lower()

        price_info = check_price_info(coin_id)
        outgoing_message = construct_message(price_info)

        telegram_outgoing_queue.put(outgoing_message)


def check_price_info(coin_id):
    # This try can be removed once the server has a newer version of Python
    try:
        ticker_result = ticker.get_ticker_result(coin_id)
    except UnicodeEncodeError:
        return

    if ticker_result is None:
        arbotrator.send_message(
            "Sorry, ik kan geen coin vinden met de naam \"{}\"".format(
                " ".join(update_result["message"]["text"].split(" ")[1:])))
        return

    mcap = nonermalize(ticker_result, "market_cap_usd")
    if mcap is not "Onbekend":
        mcap = "$" + mcap

    return ticker_result


def construct_message(price_info):
    message = \
        """
📈 *{}* 📉

*$*{} | *€*{} | *B*{}
*1u* {}% | *24u* {}% | *7d* {}%

Market cap *USD*: {}
Voorraad: {} / {}

_Prijs van {}_
https://coinmarketcap.com/currencies/{}
        """.format(price_info["name"],
                   price_info["price_usd"],
                   price_info["price_eur"],
                   price_info["price_btc"],
                   price_info["percent_change_1h"],
                   price_info["percent_change_24h"],
                   price_info["percent_change_7d"],
                   mcap,
                   nonermalize(price_info, "available_supply"),
                   nonermalize(price_info, "total_supply"),
                   my_utils
                   .convert_unix_timestamp(
                        int(price_info["last_updated"])),
                   price_info["id"])

    return message
