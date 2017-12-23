import os
import sys

import requests

import arbotrator


def check_directory():
    return "../data/litebit_checks/"


def add_check(abbr):
    if not abbr.isalpha():
        arbotrator.send_message(
            "Sorry, \"{}\" kan ik niet toevoegen. Gebruik alleen letters." \
            .format(abbr))
        return

    with open(check_directory() + abbr, "w") as abbr_file:
        arbotrator.send_message(
            "Jo, ik ga \"{}\" voor je in de gaten houden!"\
            .format(abbr))

        abbr_file.write("")


def remove_check(abbr):
    os.remove(check_directory() + abbr)


def get_litebit_coin(coin_id):
    response = \
        requests.get("https://api.litebit.eu/market/{}" \
                     .format(coin_id))

    if response.json()["success"] is False:
        if "Market not found" in response.json()["message"]:
            remove_check(coin_id)
            arbotrator.send_message(
                "He, ik zocht zojuist op LiteBit naar \"{}\", maar die kon ik niet vinden. Ik heb de check weer weggehaald." \
                .format(coin_id))

        return None

    return response.json()


def check_availability(litebit_response):
    if float(litebit_response["result"]["available"]) > 0:
        message = \
            """
🚨 *{}S* 🚨

LiteBit heeft weer {}/{} beschikbaar!

Voorraad: {}
Koopprijs *EUR*: €{}
Verkoopprijs *EUR*: €{}

https://www.litebit.eu/nl/kopen/{}

_Ik heb bij deze de check ook weer weggehaald._
            """.format(litebit_response["result"]["name"].upper(),
                       litebit_response["result"]["name"],
                       litebit_response["result"]["abbr"].upper(),
                       litebit_response["result"]["available"],
                       litebit_response["result"]["buy"],
                       litebit_response["result"]["sell"],
                       litebit_response["result"]["name"].lower())

        arbotrator.send_message(message)
        remove_check(litebit_response["abbr"])
if __name__ == "__main__":
    coins = os.listdir("../data/litebit_checks/")
    if len(coins) == 0:
        sys.exit(0)

    for coin in coins:
        litebit_response = get_litebit_coin(coin)
        if litebit_response is None:
            continue

        check_availability(litebit_response)
