import sys

import requests

import arbotrator


litebit_page = requests.get("https://www.litebit.eu/en/buy/ripple").text

if ("Checking your browser" in litebit_page):
    # Don't bother with CloudFlare protection thing
    sys.exit(0)


if ("0 available" not in litebit_page) and \
   ("Due to maintenance on other exchanges" not in litebit_page):
        arbotrator.send_message(
            """
LiteBit lijkt Ripple/XRP beschikbaar te hebben!
https://www.litebit.eu/nl/kopen/ripple"
            """)
