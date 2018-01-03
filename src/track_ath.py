import sys

import arbotrator
import my_utils
import ticker


def notify_bot(ath_result):
    message = \
        """
🚀 *{} to the moon!* 🚀 Nieuwe *all-time-high*: ${}, €{}.
https://coinmarketcap.com/currencies/{}
        """.format(
            ath_result["name"],
            ath_result["price_usd"],
            ath_result["price_eur"],
            ath_result["name"])

    arbotrator.send_message(message)


if __name__ == "__main__":
    coin_id = sys.argv[1]

    new_result = ticker.get_api_ticker_result(coin_id)
    last_ath = ticker.get_last_all_time_high(coin_id)

    if float(new_result["price_usd"]) > last_ath:
        notify_bot(new_result)
        ticker.write_all_time_high(coin_id, new_result["price_usd"])

    ticker.write_ticker_result(coin_id, new_result)
