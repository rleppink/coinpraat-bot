""" CoinMarketCap API general utilities.

General stuff that's used by multiple modules.
"""


def get_formatted_base_url(path):
    base_url = "https://api.coinmarketcap.com/v2/"
    return f"{base_url}{path}"
