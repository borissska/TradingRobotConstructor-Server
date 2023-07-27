import datetime as dt
import backtrader as bt
import pandas as pd
from backtrader_binance import BinanceStore
from FAKE_STRATEGY import StrategyJustPrintsOHLCVAndState


def get_timeframe(tf, TimeFrame):
    """Преобразуем ТФ в параметры для добавления данных по стратегии"""
    interval = 1
    _timeframe = TimeFrame.Minutes

    if tf == '1m': interval = 1
    if tf == '5m': interval = 5
    if tf == '15m': interval = 15
    if tf == '30m': interval = 30
    if tf == '1h': interval = 60
    if tf == '4h': interval = 240
    if tf == '12h': interval = 720
    if tf == '1d': _timeframe = TimeFrame.Days
    if tf == '3d': _timeframe = TimeFrame.Days
    if tf == '3d': interval = 3
    if tf == '1w': _timeframe = TimeFrame.Weeks
    if tf == '1M': _timeframe = TimeFrame.Months
    return _timeframe, interval


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    coin_target = 'USDT'
    symbol = "BTC" + coin_target

    store = BinanceStore(
        api_key="NNNN",
        api_secret="NNNN",
        coin_target=coin_target,
        testnet=False)

    broker = store.getbroker()
    cerebro.setbroker(broker)

    tf = "3d"  # '1m'  '5m' '15m' '30m' '1h' '1d' '1w'
    _t, _c = get_timeframe(tf, bt.TimeFrame)

    data_1minute = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-leftedge\{symbol}-1m.csv",
                                           separator=',',
                                           dtformat='%Y-%m-%d %H:%M:%S',
                                           compression=1,
                                           timeframe=bt.TimeFrame.Minutes,
                                           openinterest=-1,
                                           fromdate=dt.datetime(2023, 7, 9, 9, 46)
                                           )
    # data_15minutes = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-leftedge\{symbol}-15m.csv",
    #                                          separator=',',
    #                                          dtformat='%Y-%m-%d %H:%M:%S',
    #                                          compression=15,
    #                                          timeframe=bt.TimeFrame.Minutes,
    #                                          openinterest=-1,
    #                                          fromdate=dt.datetime(2023, 7, 9, 9, 46)
    #                                          )
    # data_30minutes = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-30m.csv",
    #                                          separator=',',
    #                                          dtformat='%Y-%m-%d %H:%M:%S',
    #                                          compression=30,
    #                                          timeframe=bt.TimeFrame.Minutes,
    #                                          openinterest=-1,
    #                                          fromdate=dt.date(2023, 6, 1)
    #                                          )
    # data_1hour = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-1h.csv",
    #                                      separator=',',
    #                                      dtformat='%Y-%m-%d %H:%M:%S',
    #                                      compression=60,
    #                                      timeframe=bt.TimeFrame.Minutes,
    #                                      openinterest=-1,
    #                                      fromdate=dt.date(2023, 6, 1)
    #                                      )
    # data_4hours = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-4h.csv",
    #                                       separator=',',
    #                                       dtformat='%Y-%m-%d %H:%M:%S',
    #                                       compression=240,
    #                                       timeframe=bt.TimeFrame.Minutes,
    #                                       openinterest=-1,
    #                                       fromdate=dt.date(2023, 6, 1)
    #                                       )
    # data_12hours = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-12h.csv",
    #                                        separator=',',
    #                                        dtformat='%Y-%m-%d %H:%M:%S',
    #                                        compression=720,
    #                                        timeframe=bt.TimeFrame.Minutes,
    #                                        openinterest=-1,
    #                                        fromdate=dt.date(2023, 6, 1)
    #                                        )
    # data_1day = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-1d.csv",
    #                                     separator=',',
    #                                     dtformat='%Y-%m-%d',
    #                                     compression=1,
    #                                     timeframe=bt.TimeFrame.Days,
    #                                     sessionend=dt.time(0, 0),
    #                                     openinterest=-1,
    #                                     fromdate=dt.date(2023, 6, 1)
    #                                     )
    # data_1week = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\Binance\{symbol}\{symbol}-1w.csv",
    #                                      separator=',',
    #                                      dtformat='%Y-%m-%d',
    #                                      compression=1,
    #                                      timeframe=bt.TimeFrame.Weeks,
    #                                      sessionend=dt.time(0, 0),
    #                                      openinterest=-1,
    #                                      fromdate=dt.date(2023, 6, 1)
    #                                      )

    from_date = dt.datetime.utcnow() - dt.timedelta(minutes=5000)
    data_live_1minute = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol,
                                      start_date=from_date,
                                      LiveBars=True)
    # data_live_15minutes = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=15, dataname=symbol,
    #                                     start_date=from_date,
    #                                     LiveBars=True)
    # data_live_30minutes = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=30, dataname=symbol,
    #                                     start_date=from_date,
    #                                     LiveBars=True)
    # data_live_1hour = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=60, dataname=symbol,
    #                                 start_date=from_date,
    #                                 LiveBars=True)
    # data_live_4hours = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=240, dataname=symbol,
    #                                  start_date=from_date,
    #                                  LiveBars=True)
    # data_live_12hours = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=720, dataname=symbol,
    #                                   start_date=from_date,
    #                                   LiveBars=True)
    # data_live_1day = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol,
    #                                start_date=from_date,
    #                                LiveBars=True)
    # data_live_1week = store.getdata(timeframe=bt.TimeFrame.Weeks, compression=1, dataname=symbol,
    #                                 start_date=from_date,
    #                                 LiveBars=True)

    rollover_1minute = bt.feeds.RollOver(data_1minute, data_live_1minute, dataname=symbol,
                                         sessionend=dt.time(0, 0))
    # rollover_15minutes = bt.feeds.RollOver(data_15minutes, data_live_15minutes, dataname=symbol,
    #                                        sessionend=dt.time(0, 0))
    # rollover_30minutes = bt.feeds.RollOver(data_30minutes, data_live_30minutes, dataname=symbol,
    #                                        sessionend=dt.time(0, 0))
    # rollover_1hour = bt.feeds.RollOver(data_1hour, data_live_1hour, dataname=symbol,
    #                                    sessionend=dt.time(0, 0))
    # rollover_4hours = bt.feeds.RollOver(data_4hours, data_live_4hours, dataname=symbol,
    #                                     sessionend=dt.time(0, 0))
    # rollover_12hours = bt.feeds.RollOver(data_12hours, data_live_12hours, dataname=symbol,
    #                                      sessionend=dt.time(0, 0))
    # rollover_1day = bt.feeds.RollOver(data_1day, data_live_1day, dataname=symbol,
    #                                   sessionend=dt.time(0, 0))
    # rollover_1week = bt.feeds.RollOver(data_1week, data_live_1week, dataname=symbol,
    #                                    sessionend=dt.time(0, 0))

    cerebro.adddata(rollover_1minute)
    # cerebro.adddata(rollover_15minutes)
    # cerebro.adddata(rollover_30minutes)
    # cerebro.adddata(rollover_1hour)
    # cerebro.adddata(rollover_4hours)
    # cerebro.adddata(rollover_12hours)
    # cerebro.adddata(rollover_1day)
    # cerebro.adddata(rollover_1week)

    # cerebro.resampledata(data_live_minute, compression=15, timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data_live_minute, compression=30, timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data_live_minute, compression=60, timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data_live_minute, compression=240, timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data_live_minute, compression=720, timeframe=bt.TimeFrame.Minutes)
    # cerebro.resampledata(data_live_minute, compression=1, timeframe=bt.TimeFrame.Days)
    # cerebro.resampledata(data_live_minute, compression=1, timeframe=bt.TimeFrame.Weeks,
    #                      sessionend=dt.time(0, 0),)

    cerebro.addstrategy(StrategyJustPrintsOHLCVAndState, coin_target=coin_target)

    cerebro.run()
    cerebro.plot()
