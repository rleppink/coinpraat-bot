from flask import Flask

from flask import abort
from flask import request

import arbotrator
import ticker


app = Flask("CoinpraatValet")


def get_webhook_token():
    with open("../private/webhook_token", "r") as webhook_token_file:
        return webhook_token_file.read().strip()


def auth_path(url):
    return "/{}/{}/".format(get_webhook_token(), url)


@app.route("/")
def hello():
    return "Hello!"


@app.route(auth_path("updates"), methods=["POST"])
def listen_closely():
    if "message" not in request.get_json():
        abort(405)

    if request.get_json()["message"]["text"].startswith("/prijs"):
        coin_id = request.get_json()["message"]["text"].split(" ")[1]

        result = ticker.get_api_ticker_result(coin_id)
        arbotrator \
            .send_message("Hi {}, {} is op dit moment *USD*: {}"
                          .format(
                              request.get_json()
                              ["message"]["from"]["first_name"],
                              result["name"],
                              result["price_usd"]))

    return ""


@app.errorhandler(404)
def unknown(error):
    abort(401)


if __name__ == "__main__":
    context = ("../private/cert.pem", "../private/key.pem")
    app.run(
        host="0.0.0.0",
        port=44345,
        ssl_context=context,
        threaded=True,
        debug=True)
