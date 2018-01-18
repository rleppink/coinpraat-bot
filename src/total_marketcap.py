import requests

import my_utils


def total_marketcap_url(start, end):
    return \
        "https://graphs2.coinmarketcap.com/global/marketcap-total/{}/{}/" \
        .format(start, end)


def get_marketcap_data(start, end):
    url = total_marketcap_url(start, end)
    data = requests.get(url).json()

    if not data:
        return None

    if "market_cap_by_available_supply" not in data:
        return None

    if data["market_cap_by_available_supply"] == []:
        return None

    return data["market_cap_by_available_supply"]


def parse_marketcap_data_hours(hours):
    start = my_utils.current_unix_timestamp() - \
            my_utils.hours_in_milliseconds(hours)
    end = my_utils.current_unix_timestamp()

    data = get_marketcap_data(start, end)

    first = data[:1][0][1]
    last = data[-1:][0][1]
    total = last

    return (first, last, total)


def percent_difference(marketcap_data):
    first = marketcap_data[0]
    last = marketcap_data[1]
    return ((last / first) * 100) - 100


def get_market_differences():
    h1 = parse_marketcap_data_hours(1)
    h24 = parse_marketcap_data_hours(24)
    d7 = parse_marketcap_data_hours(24 * 7)

    return (
        percent_difference(h1),
        percent_difference(h24),
        percent_difference(d7),
        h1[2])


if __name__ == "__main__":
    print(get_market_differences())
