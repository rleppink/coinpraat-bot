import humanize

import shared

from . import listings
from . import ticker


def get_price_message(config, coin_name_or_symbol):
    coin_listing = listings.get_listing(config, coin_name_or_symbol)
    if coin_listing is None:
        return _no_listing_message(coin_name_or_symbol)

    coin_id = coin_listing.id

    ticker_data = ticker.get_ticker_data(config, coin_id)
    if ticker_data is None:
        return _unable_to_get_ticket_data(coin_name_or_symbol)

    return _construct_price_message(ticker_data.data)


def _no_listing_message(coin_name_or_symbol):
    return f"Hmm, ik kon geen vermelding vinden voor {coin_name_or_symbol}."


def _unable_to_get_ticket_data(coin_name_or_symbol):
    return f"He sorry, ik kon geen data vinden voor {coin_name_or_symbol}. Mogelijk is de CoinmarketCap API tijdelijk niet beschikbaar."


def _construct_price_message(ticker_data):
    def humanized(big_number):
        if big_number is None:
            return None

        return humanize.intword(int(float(big_number)))

    message = \
        f"""
📈 *{ticker_data.name}* 📉

*$*{ticker_data.quotes.USD.price} | *€*{ticker_data.quotes.EUR.price}
*1u* {ticker_data.quotes.USD.percent_change_1h}% | *24u* {ticker_data.quotes.USD.percent_change_24h}% | *7d* {ticker_data.quotes.USD.percent_change_7d}%

Market cap *USD*: ${humanized(ticker_data.quotes.USD.market_cap)}
Market cap *EUR*: €{humanized(ticker_data.quotes.EUR.market_cap)}
Voorraad: {humanized(ticker_data.circulating_supply)} / {humanized(ticker_data.total_supply)}

_Prijs van {shared.utilities.human_readable_unix_timestamp(ticker_data.last_updated)}_
https://coinmarketcap.com/currencies/{ticker_data.website_slug}/
        """

    return message
