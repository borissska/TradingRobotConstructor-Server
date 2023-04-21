import backtrader as bt


class TestStrategy(bt.Strategy):

    def __init__(self, strategy):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        for el in strategy["elements"]:
            if el.element_type == "sma":
                period = 10
                if el.parameter_name_id == "period":
                    period = el.parameter_value
                self.rsi = bt.talib.tafunc.SMA(self.data_close, period=period)

        self.sma_1 = bt.talib.SMA()
        if True:
            self.rsi = bt.indicators.RelativeStrengthIndex(

            )
        self.macd = bt.indicators.MACD(

        )
        self.momentum = bt.indicators.Momentum(

        )
        self.bollinger = bt.indicators.BollingerBands(
        )
        self.sma = bt.indicators.SMA(
            self.datas[0], period=10
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data_close[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.data_close[0])
                self.order = self.buy()

        else:
            if self.data_close[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.data_close[0])
                self.order = self.sell()