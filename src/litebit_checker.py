import requests

import arbotrator


litebit_page = requests.get("https://www.litebit.eu/en/buy/ripple").text

if ("0 available" not in litebit_page) and \
   ("Due to maintenance on other exchanges" not in litebit_page):
        arbotrator.send_message(
            """
LiteBit lijkt Ripple/XRP bescihkbaar te hebben!
https://www.litebit.eu/nl/kopen/ripple"
            """)
else:
    print("Nothing, sorry")
