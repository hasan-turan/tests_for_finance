from datetime import datetime

import numpy
import numpy as np


def to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)


def np_datetime_to_datetime(np_datetime: numpy.datetime64):
    return np_datetime.astype('datetime64[s]').item()


def np_datetime_to_string(np_datetime: numpy.datetime64, format: str):
    return np_datetime_to_datetime(np_datetime).strftime(format)
