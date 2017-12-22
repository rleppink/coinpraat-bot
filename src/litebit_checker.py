import sys

import requests

import arbotrator


def get_litebit_ripple():
    return requests.get("https://api.litebit.eu/market/xrp")


if __name__ == "__main__":
    response = get_litebit_ripple()
    if response.json()["success"] is False:
        sys.exit(0)

    if float(response.json()["result"]["available"]) > 0:
        message = \
            """
🚨 *RIPPLES!* 🚨

LiteBit heeft Ripple/XRP beschikbaar!
Koopprijs *EUR*: €{}
Verkoopprijs *EUR*: €{}

https://www.litebit.eu/nl/kopen/ripple
            """.format(response.json()["result"]["buy"],
                       response.json()["result"]["sell"])

        arbotrator.send_message(message)
    else:
        print("Sorry, kid.")
