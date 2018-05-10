import time

import requests

from shared.messages import MessageType
from . import utilities


def handler(config, outgoing_queue):
    print("[OUT-] Started Telegram outgoing handler...")
    while True:
        outgoing_message = outgoing_queue.get()

        url = data = None

        if outgoing_message.message_type == MessageType.TEXT:
            url, data = construct_text_url_and_data(config, outgoing_message)

        elif outgoing_message.message_type == MessageType.TYPING:
            url, data = construct_typing_url_and_data(config,
                                                      outgoing_message.chat_id)

        try:
            requests.post(url, data).json()
        except requests.exceptions.RequestException:
            # TODO: Better mechanism. For now, just keep retrying, whatever.
            outgoing_queue.put(outgoing_message)
            time.sleep(1)


def construct_text_url_and_data(config, outgoing_message):
    return (utilities.telegram_bot_url(config) + "sendMessage", {
        "chat_id": outgoing_message.chat_id,
        "text": outgoing_message.message,
        "reply_to_message_id": outgoing_message.reply_to_id,
        "disable_web_page_preview": "true",
        "parse_mode": "markdown",
    })


def construct_typing_url_and_data(config, chat_id):
    return (utilities.telegram_bot_url(config) + "sendChatAction", {
        "chat_id": chat_id,
        "action": "typing"
    })
