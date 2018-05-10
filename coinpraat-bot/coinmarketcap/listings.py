""" CoinMarketCap API listings interface. """
import json
import os

import requests

from . import utilities


class Listing:
    """ A listing on the CMC API. """

    def __init__(self, id, name, symbol, website_slug):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.website_slug = website_slug

    def __repr__(self):
        return f"(Listing {self.id}, {self.name}, {self.symbol}, {self.website_slug})"


def get_listing_information(config, name):
    """
    Search a given name or symbol in CMC listings.
    Return the name or symbol's listing information.
    """
    cached_listings = _get_cached_listings(config)
    if cached_listings is not None:
        listing = _search_in_listings(cached_listings, name)
        if listing is not None:
            print("Cache hit!")
            return _listing_from_json(listing)

    updated_listings = _get_updated_listings()
    if updated_listings is None:  # There is just nothing we can do.
        return None

    _cache_updated_listings(config, updated_listings)

    listing = _search_in_listings(updated_listings, name)
    if listing is None:
        return None

    return _listing_from_json(listing)


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
    try:
        listings_url = utilities.get_formatted_base_url("listings")
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


def _listing_from_json(listing_json):
    return Listing(
        id=listing_json["id"],
        name=listing_json["name"],
        symbol=listing_json["symbol"],
        website_slug=listing_json["website_slug"],
    )
