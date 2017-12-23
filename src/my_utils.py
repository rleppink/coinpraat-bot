from datetime import datetime

import tzlocal


def convert_unix_timestamp(unix_timestamp):
    return \
        datetime \
        .fromtimestamp(unix_timestamp, tzlocal.get_localzone()) \
        .strftime("%Y-%m-%d %H:%M:%S (%Z)")
