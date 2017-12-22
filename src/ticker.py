import json

import requests


def get_api_ticker_result(coin_id):
    tickerUrl = \
        "https://api.coinmarketcap.com/v1/ticker/{0}/?convert=EUR"\
        .format(coin_id)

    return requests.get(tickerUrl).json()[0]


def ticker_result_path(coin_id):
    return "../data/ticker_results/{}.json".format(coin_id)


def get_last_ticker_result(coin_id):
    with open(ticker_result_path(coin_id), "r") as ticker_file:
        return json.loads(ticker_file.read())


def write_ticker_result(coin_id, result):
    with open(ticker_result_path(coin_id), "w") as ticker_file:
        json.dump(result, ticker_file)


def all_time_high_path(coin_id):
    return "../data/all_time_highs/{}.ath".format(coin_id)


def get_last_all_time_high(coin_id):
    try:
        with open(all_time_high_path(coin_id), "r") as all_time_high_file:
            return float(all_time_high_file.read().strip())
    except FileNotFoundError:
        write_all_time_high(coin_id, 0.0)
        return 0.0


def write_all_time_high(coin_id, ath_price_usd):
    with open(all_time_high_path(coin_id), "w") as all_time_high_file:
        all_time_high_file.write(str(ath_price_usd))
