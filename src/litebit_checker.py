import sys

import requests

import arbotrator


def get_litebit_coin(coin_id):
    return requests.get("https://api.litebit.eu/market/{}".format(coin_id))


if __name__ == "__main__":
    if len(sys.argv) is 1:
        print("Need an argument")
        sys.exit(1)

    coin_id = sys.argv[1]
    response = get_litebit_coin(coin_id)

    if response.json()["success"] is False:
        sys.exit(0)

    if float(response.json()["result"]["available"]) > 0:
        message = \
            """
🚨 *{}S* 🚨

LiteBit heeft weer {}/{} beschikbaar!

Voorraad: {}
Koopprijs *EUR*: €{}
Verkoopprijs *EUR*: €{}

https://www.litebit.eu/nl/kopen/{}
            """.format(
                       response.json()["result"]["name"].upper(),
                       response.json()["result"]["name"],
                       response.json()["result"]["abbr"].upper(),
                       response.json()["result"]["available"],
                       response.json()["result"]["buy"],
                       response.json()["result"]["sell"],
                       response.json()["result"]["name"].lower())

        arbotrator.send_message(message)
