from flask import Flask
from flask import abort
from flask import request

import arbotrator
import my_utils
import ticker


app = Flask("CoinpraatValet")


def get_webhook_token():
    with open("../private/webhook_token", "r") as webhook_token_file:
        return webhook_token_file.read().strip()


def auth_path(url):
    return "/{}/{}/".format(get_webhook_token(), url)


@app.route("/wh")
def hello():
    print(request.get_json())
    return "Ok!"


@app.route(auth_path("get_coin"), methods=["POST"])
def get_coin():
    if "message" not in request.get_json():
        abort(405)

    if request.get_json()["message"]["text"].startswith("/prijs"):
        coin_id = request.get_json()["message"]["text"].split(" ")[1]

        result = ticker.get_ticker_result(coin_id)

        message = \
                """
📈 *{}* 📉

Huidige prijs *USD*: ${}
Huidige prijs *EUR*: €{}
Huidige prijs *BTC*: B{}

Verandering *1u*: {}%
Verandering *24u*: {}%
Verandering *7d*: {}%

_Prijs van {}_
                """.format(result["name"],
                           result["price_usd"],
                           result["price_eur"],
                           result["price_btc"],
                           result["percent_change_1h"],
                           result["percent_change_24h"],
                           result["percent_change_7d"],
                           my_utils \
                           .convert_unix_timestamp(
                               int(result["last_updated"])))

        arbotrator.send_message(message)

    return ""


@app.errorhandler(404)
def unknown(error):
    abort(401)


if __name__ == "__main__":
    context = ("../private/cert.pem", "../private/key.pem")
    app.run(
        host="0.0.0.0",
        port=8443,
        ssl_context=context,
        threaded=True,
        debug=True)
