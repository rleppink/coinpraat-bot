def telegram_bot_url(config):
    bot_token = config["telegram_bot_token"]
    default_url = "https://api.telegram.org/{}{}/"

    return default_url.format(
       "" if bot_token.startswith("bot") else "bot",
       bot_token)
