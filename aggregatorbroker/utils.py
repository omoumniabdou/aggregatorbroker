from datetime import datetime

import pytz


def extract_datetime_minute(dt):
    """
    The minute (as a datetime) for the given date time
    :param dt: the date time
    :return: the minute (as a datetime)
    """
    return dt.replace(second=0, microsecond=0)


def minute_interval(dt):
    """
    The minute interval where the given date time is situated
    :param dt: the date time
    :return: the minute interval
    """
    start = extract_datetime_minute(dt)
    end = next_minute(start)
    return [start, end]


def next_minute(dt):
    """
    The next minute (as a datetime) for the given date time
    :param dt: the date time
    :return: the next minute (as a datetime)
    """
    return dt.replace(minute=dt.minute + 1)


def as_utc(dt):
    """
    Convert datetime to the UTC time zone
    :param dt: the date time
    :return: the converted date time
    """
    return dt.astimezone(tz=pytz.utc)


def now():
    """
    The now date time in the UTC time zone
    :return: the now date time
    """
    return as_utc(datetime.now())


def parse_datetime(dt_str):
    """
    Parse date time and convert it to UTC time zone
    :param dt_str: the string containing the date time
    :return: the parsed date time
    """
    return as_utc(datetime.fromisoformat(dt_str))
