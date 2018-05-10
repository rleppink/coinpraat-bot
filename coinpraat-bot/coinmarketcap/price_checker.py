import json

import ticker


def check_price_info(coin_id):
    ticker_result = ticker.get_ticker_result(coin_id)

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
