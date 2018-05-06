from enum import Enum


class OutgoingMessage:
    def __init__(self, message_type, message, chat_id, reply_to_id):
        self.message_type = message_type
        self.message = message
        self.chat_id = chat_id
        self.reply_to_id = reply_to_id


class MessageType(Enum):
    """ Define the type of message to send to Telegram. """

    # A standard text message to be sent
    TEXT = 1

    # Set the bot's status to 'typing'
    TYPING = 2
