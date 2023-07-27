import backtrader as bt
from backtrader.indicators import movav


class TEST_INDICATORS(bt.Strategy):

    def __init__(self, params=None):
        self.bar_executed = None
        self.data = self.datas[0]
        self.full_weight = 0
        self.sma_exist = False
        self.ema_exist = False
        self.rsi_exist = False
        self.bband_exist = False
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        if params is not None:
            for i in range(len(params)):
                print(params[i])
                el_type, name, value, interval, weight = params[i]
                setattr(self.params, "indicator", el_type)
                setattr(self.params, "name", name)
                setattr(self.params, "value", value)
                setattr(self.params, "interval", interval)
                setattr(self.params, "weight", weight)
                if self.p.indicator == 'sma':
                    print("Sma created!")
                    self.sma = bt.ind.SMA(self.data.close, period=int(self.p.value[0]))
                    self.sma_interval = self.p.interval
                    self.sma_weight = self.p.weight
                    self.full_weight += self.sma_weight
                    self.sma_exist = True

                elif self.p.indicator == 'ema':
                    print("Ema created!")
                    self.ema = bt.ind.EMA(self.data.close, period=int(self.p.value[0]))
                    self.ema_interval = self.p.interval
                    self.ema_weight = self.p.weight
                    self.full_weight += self.ema_weight
                    self.ema_exist = True

                elif self.p.indicator == 'bband':
                    print("Bbands created!")
                    self.bband = bt.ind.BollingerBands(self.data.close, period=int(self.p.value[0]),
                                                       devfactor=float(self.p.value[1]))
                    self.bband_interval = self.p.interval
                    self.bband_weight = self.p.weight
                    self.full_weight += self.bband_weight
                    self.bband_exist = True

                elif self.p.indicator == 'rsi' and self.rsi_exist:
                    self.rsi_buy = self.p.value

                elif self.p.indicator == 'rsi':
                    self.rsi = bt.ind.RSI(self.data.close)
                    self.rsi_interval = self.p.interval
                    self.rsi_weight = self.p.weight
                    self.rsi_sell = self.p.value
                    self.full_weight += self.rsi_weight
                    self.rsi_exist = True

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

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
            else:  # Sell
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
            if self.sma_exist:
                if self.sma[0] < self.data[0]:
                    self.order = self.buy()
            if self.ema_exist:
                if self.ema[0] < self.data[0]:
                    self.order = self.buy()

            if self.bband_exist:
                if self.bband.bot > self.data[0]:
                    self.order = self.buy()

        else:
            if self.sma_exist:
                if self.sma[0] > self.data[0]:
                    self.order = self.sell()
            if self.ema_exist:
                if self.ema[0] > self.data[0]:
                    self.order = self.sell()

            if self.bband_exist:
                if self.bband.top < self.data[0]:
                    self.order = self.sell()
