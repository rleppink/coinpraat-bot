""" CoinMarketCap Ticker API interface

This endpoint displays cryptocurrency ticker data in order of rank. The maximum
number of results per call is 100. Pagination is possible by using the start
and limit parameters.

For more information: https://coinmarketcap.com/api/#endpoint_ticker
"""

import json
import os
import time

import munch
import requests

from . import utilities


def get_ticker_data(config, coin_id):
    """
    Retrieve ticker data for the given coin id.
    If there is cached data for this coin id that's less than 5 minutes old,
    that data will be returned. If not, returns updated data straight from the
    API.
    """

    cached_ticker_data = _get_cached_ticker_data(config, coin_id)
    if cached_ticker_data is not None and _less_than_5_minutes_ago(
            cached_ticker_data["metadata"]["timestamp"]):
        return munch.Munch.fromDict(cached_ticker_data)

    updated_ticker_data = _get_updated_ticker_data(coin_id)
    if updated_ticker_data is None:
        return None

    _cache_ticker_data(config, updated_ticker_data)

    return munch.Munch.fromDict(updated_ticker_data)


def _get_cached_ticker_data(config, coin_id):
    """
    Attempt to get cached coin data from the cache directory. It is saved in
    and returned in JSON format.
    """
    ticker_data_path = _ticker_data_directory(config) + str(coin_id)

    try:
        with open(ticker_data_path, "r") as ticker_data_file:
            cached_ticker_data = ticker_data_file.read()
            return json.loads(cached_ticker_data)
    except FileNotFoundError:
        return None


def _get_updated_ticker_data(coin_id):
    """
    Attempt to retrieve new ticker data from the CMC API. If not found or
    any error occurs, return None.
    """

    ticker_url = utilities.get_formatted_base_url(
        f"/ticker/{coin_id}/?convert=EUR")

    try:
        response = requests.get(ticker_url)
        if response is None:
            return None

        return response.json()
    except requests.exceptions.RequestException:
        return None


def _cache_ticker_data(config, ticker_data):
    """
    Cache ticker data results. CMC ticker endpoint is updated once every 5
    minutes, so callling the API multiple times in 5 minutes is useless. Cached
    ticker data is saved with the coin's id as the filename in the cache
    directory.
    """

    cache_directory = _ticker_data_directory(config)
    ticker_data_path = cache_directory + str(ticker_data["data"]["id"])

    # Can throw an exception, but if I can't make a cache, we might aswell just
    # quit the whole operation
    os.makedirs(cache_directory, exist_ok=True)

    try:
        with open(ticker_data_path, "w") as ticker_data_file:
            json.dump(ticker_data, ticker_data_file)
            return True
    except IOError:
        return None


def _ticker_data_directory(config):
    return config.data_path + "coinmarketcap/cached_ticker_data/"


def _less_than_5_minutes_ago(timestamp):
    timestamp_now = int(time.time())
    five_minutes = 60 * 5

    return timestamp + five_minutes > timestamp_now
