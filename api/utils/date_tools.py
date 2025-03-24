import datetime

def add_remove_hours_with_tz(date, hours, add=False, remove=False):
    """
    Add a hours to the date.

    This takes care of historic offset changes and DST.

    Parameters
    ----------
    date : timezone-aware datetime object

    Returns
    -------
    new_date : timezone-aware datetime object
    """
    today_utc = date.astimezone(datetime.timezone.utc)
    tz = date.tzinfo
    if add:
        tomorrow_utc = today_utc + datetime.timedelta(days=hours // 24, hours= hours % 24)
    elif remove:
        tomorrow_utc = today_utc - datetime.timedelta(days=hours // 24, hours= hours % 24)
    tomorrow_utc_tz = tomorrow_utc.astimezone(tz)
    tomorrow_utc_tz = tomorrow_utc_tz.replace(hour=date.hour,
                                              minute=date.minute,
                                              second=date.second)
    print(tomorrow_utc_tz)
    return tomorrow_utc_tz


def hours_to_datetime_with_tz(hours: int):
    naive_datetime = datetime.timedelta(days=hours // 24, hours= hours % 24)
    aware_datetime = naive_datetime.replace(tzinfo=datetime.timezone.utc)
    return aware_datetime
