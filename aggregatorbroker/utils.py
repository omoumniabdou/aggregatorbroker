def extract_datetime_minute(dt):
    return dt.replace(second=0, microsecond=0)
