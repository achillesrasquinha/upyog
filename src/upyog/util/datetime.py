# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import time
import datetime as dt
import math

from upyog.util._math import sign

now         = dt.datetime.now
utcnow      = dt.datetime.utcnow
timedelta   = dt.timedelta
datetime    = dt.datetime

try:
    import pytz
    timezone = pytz.timezone
except ImportError:
    pass

weekday     = dt.datetime.weekday
iso_weekday = dt.datetime.isoweekday

_DEFAULT_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_timestamp_str(format_ = _DEFAULT_TIMESTAMP_FORMAT):
    """
    Get current timestamp string.

    :param format_: Python-compatible datetime format. (optional)

    Example:
        
        >>> upy.get_timestamp_str()
        '2021-09-15 14:24:11'
        >>> upy.get_timestamp_str(format_ = '%d/%m/%Y')
        '15/09/2021'
    """
    now       = time.time()
    
    datetime_ = dt.datetime.fromtimestamp(now)
    string    = datetime_.strftime(format_)

    return string

def check_datetime_format(datetime, format_, raise_err = False):
    """
    Check if a given "date-string" is of the format given.

    :param datetime: Datetime string.
    :param format: Python-compatible datetime format.
    :param raise_err: Raise a `ValueError` in case the format is not compliant.

    :return: bool
    :raises: ValueError

    Example:

        >>> upy.check_datetime_format('2011-11-11', '%Y-%m-%d')
        True
        >>> upy.check_datetime_format('2011-11-11 11:12:13', '%Y-%m-%d')
        False
        >>> upy.check_datetime_format('2011-11-11 11:12:13', '%Y-%m-%d', raise_err = True)
        ValueError: Incorrect datetime format, expected %Y-%m-%d
    """
    try:
        dt.datetime.strptime(datetime, format_)
    except ValueError:
        if raise_err:
            raise ValueError("Incorrect datetime format, expected %s" % format_)
        else:
            return False
    
    return True

_AUTO_FORMATS = [
    '%Y-%m-%d %H:%M:%S.%f%z',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%Y-%m-%d',
    '%Y-%m',
    '%Y',
    '%d-%m-%Y %H:%M:%S.%f%z',
    '%d-%m-%Y %H:%M:%S.%f',
    '%d-%m-%Y %H:%M:%S',
    '%d-%m-%Y %H:%M',
    '%d-%m-%Y',
    '%H:%M:%S.%f%z',
    '%H:%M:%S.%f',
    '%H:%M:%S',
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%dT%H:%M:%S.%f%z'
]

def auto_datetime(string):
    """
        Convert string to datetime object
    """
    if isinstance(string, dt.datetime):
        return string

    for format_ in _AUTO_FORMATS:
        try:
            return dt.datetime.strptime(string, format_)
        except ValueError:
            pass

    raise ValueError("Incorrect datetime format, expected %s" % _AUTO_FORMATS)

def start_of(dt, type_):
    diff = None

    if "week" in type_:
        if type_.startswith("iso"):
            td_args = { "days" : dt.isoweekday() - 1 }
        else:
            td_args = { "days" : dt.weekday() }
        
        diff = dt - timedelta(**td_args)
    elif type_ == "year":
        diff = dt - timedelta(days = dt.timetuple().tm_yday - 1)
    else:
        raise ValueError("Invalid type: %s" % type_)

    norm = diff.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    return norm

def add(dt, value, type_):
    if type_ == "year":
        type_ = "days"
        value = sign(value) * 365 # TODO: Handle leap years

    return dt + timedelta(**{ type_: value })

def subtract(dt, value, type_):
    return add(dt, -value, type_)

def iso_weekday(dt, diff):
    return add(dt, diff, "days")

def str2timedelta(string):
    dt = auto_datetime(string)
    return timedelta(
        days    = dt.day - 1,
        hours   = dt.hour,
        minutes = dt.minute,
        seconds = dt.second,
        microseconds = dt.microsecond
    )

def format(dt, format_):
    return dt.strftime(format_)

def ts(dt):
    return time.mktime(dt.timetuple())

def human_datetime(dt, year = True):
    dt = auto_datetime(dt)

    format_ = "%b %d, "
    if year:
        format_ += "%Y "
    format_ += "%I:%M %p"

    return dt.strftime(format_)