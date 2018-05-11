from datetime import datetime
import types

import tzlocal
import yaml


def human_readable_unix_timestamp(unix_timestamp):
    return \
        datetime \
        .fromtimestamp(unix_timestamp, tzlocal.get_localzone()) \
        .strftime("%Y-%m-%d %H:%M:%S (%Z)")


def read_config():
    config_path = "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        return types.SimpleNamespace(**config)
