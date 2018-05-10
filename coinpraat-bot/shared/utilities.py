from datetime import datetime
import time
import types

import tzlocal
import yaml


def convert_unix_timestamp(unix_timestamp):
    return \
        datetime \
        .fromtimestamp(unix_timestamp, tzlocal.get_localzone()) \
        .strftime("%Y-%m-%d %H:%M:%S (%Z)")


def current_unix_timestamp():
    # 1516175220000
    return int(time.mktime(time.gmtime())) * 1000


def hours_in_milliseconds(hours):
    return hours * 60 * 60 * 1000


def read_config():
    config_path = "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        return types.SimpleNamespace(**config)
