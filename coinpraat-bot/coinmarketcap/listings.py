""" CoinMarketCap Listings API interface.

This endpoint displays all active cryptocurrency listings in one call. Use the
"id" field on the Ticker endpoint to query more information on a specific
cryptocurrency.

For more information: https://coinmarketcap.com/api/#endpoint_listings
"""

import json
import os

import munch
import requests

from . import utilities


def get_listing(config, name):
    """
    Search a given name or symbol in CMC listings.
    Return the name or symbol's listing information.
    """
    cached_listings = _get_cached_listings(config)
    if cached_listings is not None:
        listing = _search_in_listings(cached_listings, name)
        if listing is not None:
            return munch.Munch.fromDict(listing)

    updated_listings = _get_updated_listings()
    if updated_listings is None:  # There is just nothing we can do.
        return None

    _cache_updated_listings(config, updated_listings)

    listing = _search_in_listings(updated_listings, name)
    if listing is None:
        return None

    return munch.Munch.fromDict(listing)


def _search_in_listings(listings, name):
    try:
        listing = next(listing for listing in listings
                       if listing["name"].lower() == name.lower()
                       or listing["symbol"].lower() == name.lower()
                       or listing["website_slug"].lower() == name.lower())

        return listing
    except StopIteration:
        return None


def _get_updated_listings():
    listings_url = utilities.get_formatted_base_url("listings")

    try:
        response = requests.get(listings_url)
        if response is None:
            return None

        if response.json() is None:
            return None

        return response.json()["data"]
    except requests.exceptions.RequestException:
        return None


def _get_cached_listings(config):
    try:
        with open(config.data_path + "coinmarketcap/cached_listings",
                  "r") as cached_listings_file:
            cached_listings_str = cached_listings_file.read()
            return json.loads(cached_listings_str)
    except IOError:
        return None
    except json.decoder.JSONDecodeError:
        return None


def _cache_updated_listings(config, listings):
    # Can throw an exception, but if I can't make a cache, we might aswell just
    # quit the whole operation
    os.makedirs(config.data_path + "coinmarketcap", exist_ok=True)

    try:
        with open(config.data_path + "coinmarketcap/cached_listings",
                  "w") as cached_listings_file:
            json.dump(listings, cached_listings_file)
            return True
    except IOError:
        return None
