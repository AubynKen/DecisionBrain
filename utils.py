# this file contains utility functions used in the project

from datetime import datetime


def parse_time(time):
    if type(time) == str:
        return datetime.strptime(time, '%I:%M%p')
    return time
