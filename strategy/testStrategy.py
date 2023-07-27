import backtrader as bt
import datetime as dt
from strategy.strategy import Strategy
from strategy.FAKE_STRATEGY import StrategyJustPrintsOHLCVAndState


def get_timeframe(tf, TimeFrame):
    """Преобразуем ТФ в параметры для добавления данных по стратегии"""
    interval = 1
    _timeframe = TimeFrame.Minutes

    if tf == '1m': interval = 1
    if tf == '5m': interval = 5
    if tf == '15m': interval = 15
    if tf == '30m': interval = 30
    if tf == '1h': interval = 60
    if tf == '1d': _timeframe = TimeFrame.Days
    if tf == '1w': _timeframe = TimeFrame.Weeks
    return _timeframe, interval


def testStrategy(ticker, cash, percent_of_capital, strategy, commission, strategy_name, store):
    cerebro = bt.Cerebro()

    broker = store.getbroker()
    cerebro.setbroker(broker)

    tf = "1m"  # '1m'  '5m' '15m' '30m' '1h' '1d' '1w' '1M'
    _t, _c = get_timeframe(tf, bt.TimeFrame)

    timeframe_minute = "1m"
    data_minute = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\{ticker}\{ticker}-{timeframe_minute}.csv",
                                          separator=',',
                                          dtformat='%Y-%m-%d %H:%M:%S',
                                          timeframe=bt.TimeFrame.Minutes,
                                          openinterest=-1
                                          )

    from_date = dt.datetime.utcnow() - dt.timedelta(days=5)
    data_live_minute = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=ticker, start_date=from_date, LiveBars=False)
    rollover = bt.feeds.RollOver(data_minute, data_live_minute, dataname=ticker, sessionend=dt.time(0, 0, 0))
    cerebro.resampledata(rollover, compression=15, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(rollover, compression=30, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(rollover, compression=60, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(rollover, compression=240, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(rollover, compression=720, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(rollover, compression=1, timeframe=bt.TimeFrame.Days)
    cerebro.resampledata(rollover, compression=1, timeframe=bt.TimeFrame.Weeks)

    # cerebro.addstrategy(Strategy, strategy)
    cerebro.addstrategy(StrategyJustPrintsOHLCVAndState, coin_target="USDT")
    cerebro.addsizer(bt.sizers.PercentSizer, percents=int(percent_of_capital))

    cerebro.run()
    cerebro.plot()

    max_loss = 0
    profit_per_year = cerebro.broker.getvalue()
    full_profit = cerebro.broker.getvalue()

    return max_loss, profit_per_year, full_profit