import backtrader as bt
from backtrader.utils import date2num
from datetime import datetime, time, timedelta


def getstarttime(timeframe, compression, dt, sessionstart=None, offset=0):
    '''
    This method will return the start of the period based on current
    time (or provided time).
    '''
    if sessionstart is None:
        # use UTC 22:00 (5:00 pm New York) as default
        sessionstart = time(hour=0, minute=0, second=0)
    if dt is None:
        dt = datetime.utcnow()
    if timeframe == bt.TimeFrame.Seconds:
        dt = dt.replace(
            second=(dt.second // compression) * compression,
            microsecond=0)
        if offset:
            dt = dt - timedelta(seconds=compression*offset)
    elif timeframe == bt.TimeFrame.Minutes:
        if compression >= 60:
            hours = 0
            minutes = 0
            # get start of day
            dtstart = getstarttime(bt.TimeFrame.Days, 1, dt, sessionstart)
            # diff start of day with current time to get seconds
            # since start of day
            dtdiff = dt - dtstart
            hours = dtdiff.seconds//((60*60)*(compression//60))
            minutes = compression % 60
            dt = dtstart + timedelta(hours=hours, minutes=minutes)
        else:
            dt = dt.replace(
                minute=(dt.minute // compression) * compression,
                second=0,
                microsecond=0)
        if offset:
            dt = dt - timedelta(minutes=compression*offset)
    elif timeframe == bt.TimeFrame.Days:
        if dt.hour < sessionstart.hour:
            dt = dt - timedelta(days=1)
        if offset:
            dt = dt - timedelta(days=offset)
        dt = dt.replace(
            hour=sessionstart.hour,
            minute=sessionstart.minute,
            second=sessionstart.second,
            microsecond=sessionstart.microsecond)
    elif timeframe == bt.TimeFrame.Weeks:
        if dt.weekday() != 6:
            # sunday is start of week at 5pm new york
            dt = dt - timedelta(days=dt.weekday() + 1)
        if offset:
            dt = dt - timedelta(days=offset * 7)
        dt = dt.replace(
            hour=sessionstart.hour,
            minute=sessionstart.minute,
            second=sessionstart.second,
            microsecond=sessionstart.microsecond)
    elif timeframe == bt.TimeFrame.Months:
        if offset:
            dt = dt - timedelta(days=(min(28 + dt.day, 31)))
        # last day of month
        last_day_of_month = dt.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(
            days=last_day_of_month.day)
        last_day_of_month = last_day_of_month.day
        # start of month
        if dt.day < last_day_of_month:
            dt = dt - timedelta(days=dt.day)
        dt = dt.replace(
            hour=sessionstart.hour,
            minute=sessionstart.minute,
            second=sessionstart.second,
            microsecond=sessionstart.microsecond)
    return dt


class CSVAdjustTime(bt.feeds.GenericCSVData):

    params = dict(
        adjstarttime=False,
    )

    def _loadline(self, linetokens):
        res = super(CSVAdjustTime, self)._loadline(linetokens)
        if self.p.adjstarttime:
            # move time to start time of next candle
            # and subtract 0.1 miliseconds (ensures no
            # rounding issues, 10 microseconds is minimum)
            new_date = getstarttime(
                self._timeframe,
                self._compression,
                self.datetime.datetime(0),
                self.sessionstart,
                -1) - timedelta(microseconds=100)
            self.datetime[0] = date2num(new_date)
        return res