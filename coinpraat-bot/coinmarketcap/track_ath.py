import sys

import yaml

import ticker
import shared


def handler(config, telegram_outgoing_queue):
    print("[ATHC] Started all time high checker...")
    while True:
        coin_ids_to_check = yaml.load(config.data_path + "coinmarketcap")


def check_coin(coin_id):
    coin_id = sys.argv[1]

    new_result = ticker.get_api_ticker_result(coin_id)
    last_ath = ticker.get_last_all_time_high(coin_id)

    if float(new_result["price_usd"]) > last_ath:
        return construct_message(new_result)

    return None


def construct_message(ath_result):
    return f"""
🚀 *{ath_result["name"]} to the moon!* 🚀
Nieuwe *all-time-high*: ${ath_result["price_usd"]}, €{ath_result["price_eur"]}.
https://coinmarketcap.com/currencies/{ath_result["name"]}
    """
