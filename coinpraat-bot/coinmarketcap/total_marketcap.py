import time

import humanize
import requests


def get_marketcap_message():
    differences = _get_market_differences()

    return f"""
    📈 *Totale markt* 📉
*1u*: {differences[0]:0.2f}% | *24u*: {differences[1]:0.2f}% | *7d*: {differences[2]:0.2f}%

Market cap *USD*: ${humanize.intword(int(float(differences[3])))}
https://coinmarketcap.com/charts/
    """


def _get_market_differences():
    h1 = _parse_marketcap_data_hours(1)
    h24 = _parse_marketcap_data_hours(24)
    d7 = _parse_marketcap_data_hours(24 * 7)

    return (_percent_difference(h1), _percent_difference(h24),
            _percent_difference(d7), h1[2])


def _total_marketcap_url(start, end):
    return \
        "https://graphs2.coinmarketcap.com/global/marketcap-total/{}/{}/" \
        .format(start, end)


def _parse_marketcap_data_hours(hours):
    hours_in_ms = hours * 60 * 60 * 1000
    current_unix_timestamp_ms = int(time.mktime(time.gmtime())) * 1000

    start = current_unix_timestamp_ms - hours_in_ms
    end = current_unix_timestamp_ms

    data = _get_marketcap_data(start, end)

    if data is None:
        return None

    first = data[:1][0][1]
    last = data[-1:][0][1]
    total = last

    return (first, last, total)


def _get_marketcap_data(start, end):
    url = _total_marketcap_url(start, end)
    data = requests.get(url).json()

    if not data:
        return None

    if "market_cap_by_available_supply" not in data:
        return None

    if data["market_cap_by_available_supply"] == []:
        return None

    return data["market_cap_by_available_supply"]


def _percent_difference(marketcap_data):
    if marketcap_data is None:
        return 0

    first = marketcap_data[0]
    last = marketcap_data[1]
    return ((last / first) * 100) - 100


if __name__ == "__main__":
    print(get_marketcap_message())
