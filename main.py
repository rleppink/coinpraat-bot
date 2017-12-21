import json
import sys

import requests


def get_api_ticker_result(coin_id):
    tickerUrl = \
        "https://api.coinmarketcap.com/v1/ticker/{0}/?convert=EUR"\
        .format(coin_id)

    return requests.get(tickerUrl).json()[0]


def ticker_result_path(coin_id):
    return "ticker_results/{}.json".format(coin_id)


def get_saved_ticker_result(coin_id):
    with open(ticker_result_path(coin_id), "r") as ticker_file:
        return json.loads(ticker_file.read())


def write_ticker_result(json_result):
    coin_id = json_result["id"]

    with open(ticker_result_path(coin_id), "w") as ticker_file:
        json.dump(json_result, ticker_file)

    return json_result


def all_time_high(api_result, saved_result):
    return \
        float(api_result["price_usd"]) > float(saved_result["all_time_high"])


def add_highest(api_result, saved_result):
    if "all_time_high" not in saved_result:
        saved_result["all_time_high"] = saved_result["price_usd"]

    if all_time_high(api_result, saved_result):
        print("Added highest")
        api_result["all_time_high"] = api_result["price_usd"]
        return api_result

    return saved_result


def get_secret():
    with open("secret", "r") as secret_file:
        return secret_file.read()


def get_bot_url():
    return "https://api.telegram.org/bot{}/".format(get_secret())


def notify_bot(new_result):
    message = \
        """
🚀 *To the moon!* 🚀

Ripple heeft een nieuwe *all-time-high* bereikt!

Huidige prijs *USD*: ${}
Huidige prijs *EUR*: €{}
Huidige prijs *BTC*: B{}

Stijging *1u*: {}%
Stijging *24u*: {}%
Stijging *7d*: {}%
        """.format(
            new_result["price_usd"],
            new_result["price_eur"],
            new_result["price_btc"],
            new_result["percent_change_1h"],
            new_result["percent_change_24h"],
            new_result["percent_change_7d"])

    requests.post(
        get_bot_url() + "sendMessage",
        data={'chat_id': 12974128,
              'text': message,
              'parse_mode': 'markdown'})


if __name__ == "__main__":
    coin_id = sys.argv[1]

    new_result = get_api_ticker_result(coin_id)
    saved_result = None
    try:
        saved_result = get_saved_ticker_result(coin_id)
    except FileNotFoundError:
        write_ticker_result(new_result)
        sys.exit(0)

    print(new_result)
    print(saved_result)

    if all_time_high(new_result, add_highest(new_result, saved_result)):
        notify_bot(new_result)

    write_ticker_result(add_highest(new_result, saved_result))
