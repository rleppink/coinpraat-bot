import sys

import requests


def get_telegram_bot_token():
    with open("../private/telegram_bot_token", "r") as telegram_bot_token_file:
        return telegram_bot_token_file.read().strip()


def get_chat_id():
    with open("../private/chat_id", "r") as chat_id_file:
        return chat_id_file.read().strip()


def get_bot_url():
    return "https://api.telegram.org/bot{}/".format(get_telegram_bot_token())


def send_message(message):
    url = get_bot_url() + "sendMessage"

    return requests.post(
        url,
        data={'chat_id': get_chat_id(),
              'text': message,
              'disable_web_page_preview': 'true',
              'parse_mode': 'markdown'})


def get_updates():
    return requests.get(get_bot_url() + "getUpdates")


if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == "updates" or sys.argv[1] == "-u"):
        print(get_updates().text)
    else:
        print(requests.get(get_bot_url() + "getMe").text)
