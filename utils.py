from datetime import datetime


def parse_time(time):
    if not time:
        return
    if type(time) == str:
        return datetime.strptime(time, '%I:%M%p')
    return time


def parse_time_minute(time):
    if time is None:
        return
    return int((parse_time(time) - datetime(year=1901, month=1, day=1, hour=0)).seconds / 60)
