""" Message handler.

This module handles the Telegram incoming message content.
"""
import random

import Levenshtein

import coinmarketcap
import litebit
import shared


def handler(config, incoming_message_queue, outgoing_message_queue):
    print("[IN--] Started message handler...")

    while True:
        next_message = incoming_message_queue.get()

        # We are doing stuff, set status to typing.
        outgoing_message_queue.put(
            shared.messages.OutgoingMessage(shared.messages.MessageType.TYPING,
                                            None, next_message.chat.id, None))

        bot_command = _try_get_bot_command(next_message)
        if bot_command is None:
            continue

        message = _get_message_match(bot_command[0], next_message,
                                     config.command_distance)
        if message is None:
            continue

        outgoing_message_queue.put(message)


def _try_get_bot_command(update):
    """
    Attempt to get a command from the given message. Return None if not
    succesful.
    """
    try:
        entity = update.entities[0]
        if entity.type != "bot_command":
            return None

        return update.text.split(' ', 1)
    except KeyError:
        # No message, not a bot command, etc. Not something we can or should
        # handle, so just ignore
        return None


def _get_message_match(bot_command, incoming_message, command_distance):
    message = None
    if _matches(bot_command, "/prijs", command_distance):
        message = _create_general_message(incoming_message, "Prijs check")

    elif _matches(bot_command, "/markt", command_distance):
        message = _create_general_message(incoming_message, "Markt check")

    elif _matches(bot_command, "/check", command_distance):
        message = _create_general_message(incoming_message, "LiteBit check")

    elif _matches(bot_command, "/help", command_distance):
        message = _create_general_message(incoming_message,
                                          _get_help_message())

    else:
        message = _create_general_message(incoming_message,
                                          _get_unknown_request_message())

    return message


def _matches(command, cmp_command, distance):
    return Levenshtein.distance(command, cmp_command) <= distance


def _create_general_message(incoming_message, message_text):
    return shared.messages.OutgoingMessage(
        shared.messages.MessageType.TEXT, message_text,
        incoming_message.chat.id, incoming_message.message_id)


def _get_unknown_request_message():
    messages = [
        "Sorry, die ken ik niet.", "Hmm, hier kan ik niks mee.",
        "He, ik weet niet wat je hiermee bedoelt.",
        "Bedoelde je ook iets anders?", "Probeer het nog eens."
    ]

    return random.choice(messages)


def _get_help_message():
    return """
*CoinpraatBot help*

Commands:

*/prijs {coin}*
Vraag een prijs op van een coin.

  _Voorbeelden:_
  /prijs bitcoin
  /prijs xrp


*/markt*
Vraag een 1 dag, 7 dagen, en 30 dagen verloop van de markt op.


*/check {coin}*
Houdt LiteBit in de gaten voor updates op de meegegeven coin.

  _Voorbeelden:_
  /check ripple
  /check litecoin
    """
