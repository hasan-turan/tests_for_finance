from datetime import datetime, timedelta

from enums import Interval

DATE_FORMAT = "%d.%m.%Y"
DATE_TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

END_TIME = datetime.now()
START_TIME = datetime(day=1, month=1, year=2017)  # END_TIME - timedelta(days=729)
INTERVAL = Interval.i_1d
