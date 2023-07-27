import datetime as dt
import backtrader as bt
import numpy as np

from TEST_IDICATORS import TEST_INDICATORS


def get_timeframe(tf, TimeFrame):
    """Преобразуем ТФ в параметры для добавления данных по стратегии"""
    interval = 1
    _timeframe = TimeFrame.Minutes
    test_timeframe = "1day"

    if tf == '1m':
        interval = 1
    elif tf == '5m':
        interval = 5
    elif tf == '15m':
        interval = 15
    elif tf == '30m':
        interval = 30
    elif tf == '1h':
        interval = 60
    elif tf == '4h':
        interval = 240
    elif tf == '12h':
        interval = 720
    elif tf == '1d':
        _timeframe = TimeFrame.Days
    elif tf == '3d':
        _timeframe = TimeFrame.Days
        interval = 3
    elif tf == '1w':
        _timeframe = TimeFrame.Weeks
    elif tf == '1M':
        _timeframe = TimeFrame.Months
    return _timeframe, interval, test_timeframe


def test_indicators(symbol, timeframe, indicators, path, market, value, edge):
    cerebro = bt.Cerebro()

    _t, _c, _t_t = get_timeframe(timeframe, bt.TimeFrame)
    if _t > bt.TimeFrame.Minutes:
        dtformat = '%Y-%m-%d'
    else:
        dtformat = '%Y-%m-%d %H:%M:%S'

    data = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\{market}\{symbol}\{symbol}-{edge}\{symbol}-{timeframe}.csv",
                                   separator=',',
                                   dtformat=dtformat,
                                   compression=_c,
                                   timeframe=_t,
                                   openinterest=-1,
                                   sessionend=dt.time(0, 0)
                                   )

    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=int(99))
    cerebro.broker.setcommission(commission=0.00075)
    cerebro.addstrategy(TEST_INDICATORS, indicators)
    cerebro.run()
    cerebro.plot()

    times = cerebro.broker.getvalue()/10000

    if indicators[0] == "bband":
        if times > 5:
            my_file = open(path, "a+")
            my_file.write(f"Value: {value} - Growth (in times): %.2f\n" % times)
            my_file.close()
    else:
        my_file = open(path, "a+")
        my_file.write(f"Value: {value} - Growth (in times): %.2f\n" % times)
        my_file.close()


if __name__ == "__main__":
    edge = "rightedge" # leftedge/rightedge - не важно
    symbol = "BTCUSDT"
    market = "Binance"
    timeframe = "1d"
    name = "Any"
    weight = 10

    value_from_one = 33
    value_to_one = 50
    value_from_two = 2
    value_to_two = 51
    value_from_three = 2.0
    value_to_three = 5.1
    el_type = "sma" # sma, ema, bband
    number_values = 1

    path = f"D:\ind_tests\{market}\{symbol}\{symbol}-{edge}\{symbol}-{timeframe}\{el_type}.txt"

    # for el in ['1m', '1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '3d', '1w']:
    if number_values == 1:
        for value_one in range(value_from_one, value_to_one):
            value = [value_one]
            _t, _c, _t_t = get_timeframe(timeframe, bt.TimeFrame)
            indicators = [[el_type, name, value, _t_t, weight]]
            test_indicators(symbol, timeframe, indicators, path, market, value, edge)

    elif number_values == 2:
        for value_one in range(value_from_one, value_to_one):
            for value_two in np.arange(value_from_three, value_to_three, step=0.1):
                value = [value_one, value_two]
                _t, _c, _t_t = get_timeframe(timeframe, bt.TimeFrame)
                indicators = [[el_type, name, value, _t_t, weight]]
                test_indicators(symbol, timeframe, indicators, path, market, value, edge)

    elif number_values == 2:
        for value_one in range(value_from_one, value_to_one):
            for value_two in range(value_from_two, value_to_two):
                for value_three in np.arange(value_from_three, value_to_three, step=0.1):
                    value_three = round(value_three, 1)
                    value = [value_from_one, value_two, value_three]
                    _t, _c, _t_t = get_timeframe(timeframe, bt.TimeFrame)
                    indicators = [[el_type, name, value, _t_t, weight]]
                    test_indicators(symbol, timeframe, indicators, path, market, value, edge)

