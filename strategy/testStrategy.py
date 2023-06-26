import backtrader as bt
from strategy.strategy import Strategy


def testStrategy(ticker, cash, percent_of_capital, strategy, commission, strategy_name):
    cerebro = bt.Cerebro()

    timeframe = "1m"
    data = bt.feeds.GenericCSVData(dataname=f"D:\candle_data\{ticker}\{ticker}-{timeframe}.csv",
                                   separator=',',
                                   dtformat='%Y-%m-%d %H:%M:%S',
                                   timeframe=bt.TimeFrame.Minutes,
                                   openinterest=-1
                                   )

    cerebro.addstrategy(Strategy, strategy)
    cerebro.resampledata(data, compression=1440, timeframe=bt.TimeFrame.Minutes)
    cerebro.broker.setcash(cash=int(cash))
    cerebro.addsizer(bt.sizers.PercentSizer, percents=int(percent_of_capital))
    cerebro.broker.setcommission(commission=commission)

    cerebro.run()
    cerebro.plot(path=f"C:\diplomeProject\clientApp\icons\{strategy_name}.png", save=True, show=False)

    max_loss = 0
    profit_per_year = cerebro.broker.getvalue()
    full_profit = cerebro.broker.getvalue()

    return max_loss, profit_per_year, full_profit