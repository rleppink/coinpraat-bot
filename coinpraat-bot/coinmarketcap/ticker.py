""" CoinMarketCap Ticker API interface

This endpoint displays cryptocurrency ticker data in order of rank. The maximum
number of results per call is 100. Pagination is possible by using the start
and limit parameters.

For more information: https://coinmarketcap.com/api/#endpoint_ticker
"""

import datetime
import json

import requests


def get_ticker_result(coin_id):
    cached_ticker_result = _get_cached_ticker_result(coin_id)
    if ticker_result is None or \
       ticker_result_time(ticker_result) + (60 * 5) < current_epoch_time():
        return get_api_ticker_result(coin_id)

    return ticker_result


def _get_api_ticker_result(coin_id):
    ticker_url = get_formatted_base_url(f"/ticker/{coin_id}/?convert=EUR")

    try:
        ticker_result = requests.get(ticker_url).json()[0]

        with open(ticker_result_path(coin_id), "w") as ticker_file:
            json.dump(ticker_result, ticker_file)

        return ticker_result
    except:
        return None


def _get_cached_ticker_result(coin_id):
    try:
        with open(ticker_result_path(coin_id), "r") as ticker_file:
            return json.loads(ticker_file.read())
    except FileNotFoundError:
        return None


def _ticker_result_path(coin_id):
    return "../data/ticker_results/{}.json".format(coin_id)


def _all_time_high_path(coin_id):
    return "../data/all_time_highs/{}.ath".format(coin_id)


def _get_last_all_time_high(coin_id):
    try:
        with open(all_time_high_path(coin_id), "r") as all_time_high_file:
            return float(all_time_high_file.read().strip())
    except FileNotFoundError:
        write_all_time_high(coin_id, 0.0)
        return 0.0


def _write_all_time_high(coin_id, ath_price_usd):
    with open(all_time_high_path(coin_id), "w") as all_time_high_file:
        all_time_high_file.write(str(ath_price_usd))


def _ticker_result_time(ticker_result):
    return int(ticker_result["last_updated"])


def _current_epoch_time():
    return int(datetime.datetime.utcnow().timestamp())
