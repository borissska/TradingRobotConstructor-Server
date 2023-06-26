class Stock:
    def __init__(self, *, ticker, timeframe, year=2023, month_number=2, day=2):
        self._ticker = ticker
        self._timeframe = timeframe
        self._year = year
        self._month_number = month_number
        self._day = day

    def get_ticker(self):
        return self._ticker

    def get_timeframe(self):
        return self._timeframe

    @staticmethod
    def get_str(day_or_year):
        if len(str(day_or_year)) < 2:
            return "0" + str(day_or_year)
        else:
            return str(day_or_year)

    def get_datetime(self):
        return str(self._year) + "-" + self.get_str(self._month_number) + "-" + self.get_str(self._day)

    def get_full_link_string(self):
        return self._ticker + "/" + self._timeframe + "/" + self._ticker + "-" + self._timeframe + "-" + \
               self.get_datetime()

    def set_date(self, *, year, month_number, day):
        self._year = year
        self._month_number = month_number
        self._day = day
