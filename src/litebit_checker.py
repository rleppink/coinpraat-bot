import sys

import requests

import arbotrator


response = requests.get("https://www.litebit.eu/en/buy/ripple")
litebit_page = response.text


with open("result", "w") as result_file:
    result_file.write(litebit_page.encode("ascii", "ignore").decode("ascii"))


if response.status_code is not 200 or \
   ("Checking your browser" in litebit_page) or \
   ("The web server reported a bad gateway error" in litebit_page) or \
   ("Connection timed out" in litebit_page):
    # Don't bother with CloudFlare protection thing
    print("Foiled!")
    sys.exit(0)


if (">0 available" not in litebit_page) and \
   ("Due to maintenance on other exchanges" not in litebit_page):
        arbotrator.send_message(
            """
LiteBit lijkt Ripple/XRP beschikbaar te hebben!
https://www.litebit.eu/nl/kopen/ripple
            """)
