from datetime import datetime
import json

import requests


def get_ticker_result(coin_id):
    ticker_result = get_last_ticker_result(coin_id)
    if ticker_result is None or \
       ticker_result_time(ticker_result) + (60 * 5) < current_epoch_time():
        return get_api_ticker_result(coin_id)

    return ticker_result


def get_api_ticker_result(coin_id):
    ticker_url = \
        "https://api.coinmarketcap.com/v1/ticker/{0}/?convert=EUR"\
        .format(coin_id)

    try:
        ticker_result = requests.get(ticker_url).json()[0]
        write_ticker_result(coin_id, ticker_result)
        return ticker_result
    except:
        return None


def ticker_result_path(coin_id):
    return "../data/ticker_results/{}.json".format(coin_id)


def get_last_ticker_result(coin_id):
    try:
        with open(ticker_result_path(coin_id), "r") as ticker_file:
            return json.loads(ticker_file.read())
    except FileNotFoundError:
        return None


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


def ticker_result_time(ticker_result):
    return int(ticker_result["last_updated"])


def current_epoch_time():
    return int(datetime.utcnow().timestamp())
