import backtrader as bt
from strategy.strategy import Strategy


def testStrategy(ticker, cash, percent_of_capital, strategy, commission, strategy_name):
    cerebro = bt.Cerebro()

    timeframe_minute = "1m"
    data_minute = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\{ticker}\{ticker}-{timeframe_minute}.csv",
                                          separator=',',
                                          dtformat='%Y-%m-%d %H:%M:%S',
                                          timeframe=bt.TimeFrame.Minutes,
                                          openinterest=-1
                                          )

    cerebro.resampledata(data_minute, compression=15, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data_minute, compression=30, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data_minute, compression=60, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data_minute, compression=240, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data_minute, compression=720, timeframe=bt.TimeFrame.Minutes)
    cerebro.resampledata(data_minute, compression=1, timeframe=bt.TimeFrame.Days)
    cerebro.resampledata(data_minute, compression=1, timeframe=bt.TimeFrame.Weeks)
    cerebro.addstrategy(Strategy, strategy)
    cerebro.broker.setcash(cash=int(cash))
    cerebro.addsizer(bt.sizers.PercentSizer, percents=int(percent_of_capital))
    cerebro.broker.setcommission(commission=commission)

    cerebro.run()
    cerebro.plot()

    max_loss = 0
    profit_per_year = cerebro.broker.getvalue()
    full_profit = cerebro.broker.getvalue()

    return max_loss, profit_per_year, full_profit