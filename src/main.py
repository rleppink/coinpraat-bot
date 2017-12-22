import sys

import arbotrator
import ticker


def notify_bot(ath_result):
    message = \
        """
🚀 *To the moon!* 🚀

{} heeft een nieuwe *all-time-high* bereikt!

Huidige prijs *USD*: ${}
Huidige prijs *EUR*: €{}
Huidige prijs *BTC*: B{}

Stijging *1u*: {}%
Stijging *24u*: {}%
Stijging *7d*: {}%
        """.format(
            new_result["name"],
            new_result["price_usd"],
            new_result["price_eur"],
            new_result["price_btc"],
            new_result["percent_change_1h"],
            new_result["percent_change_24h"],
            new_result["percent_change_7d"])

    arbotrator.send_message(message)


if __name__ == "__main__":
    coin_id = sys.argv[1]

    new_result = ticker.get_api_ticker_result(coin_id)
    last_ath = ticker.get_last_all_time_high(coin_id)

    if float(new_result["price_usd"]) > last_ath:
        notify_bot(new_result["price_usd"])
        ticker.write_all_time_high(coin_id, new_result["price_usd"])

    ticker.write_ticker_result(coin_id, new_result)
