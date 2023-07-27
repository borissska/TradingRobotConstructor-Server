import backtrader as bt


class Strategy(bt.Strategy):

    def __init__(self, params=None):
        self.bar_executed = None
        self.data_15m = self.datas[0]
        self.data_30m = self.datas[1]
        self.data_1h = self.datas[2]
        self.data_4h = self.datas[3]
        self.data_12h = self.datas[4]
        self.data_1d = self.datas[5]
        self.data_1w = self.datas[6]
        self.full_weight = 0
        self.sma_exist = False
        self.ema_exist = False
        self.rsi_exist = False
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        if params is not None:
            for i in range(len(params)):
                el_type, name, value, interval, weight = params[i]
                setattr(self.params, "indicator", el_type)
                setattr(self.params, "name", name)
                setattr(self.params, "value", value)
                setattr(self.params, "interval", interval)
                setattr(self.params, "weight", weight)
                if self.p.indicator == 'sma':
                    print("Sma created!")
                    if self.p.interval == '15min':
                        self.sma = bt.ind.SMA(self.data_15m.close, period=int(self.p.value))
                    elif self.p.interval == '30min':
                        self.sma = bt.ind.SMA(self.data_30m.close, period=int(self.p.value))
                    elif self.p.interval == '1hour':
                        self.sma = bt.ind.SMA(self.data_1h.close, period=int(self.p.value))
                    elif self.p.interval == '4hours':
                        self.sma = bt.ind.SMA(self.data_4h.close, period=int(self.p.value))
                    elif self.p.interval == '12hours':
                        self.sma = bt.ind.SMA(self.data_12h.close, period=int(self.p.value))
                    elif self.p.interval == '1day':
                        self.sma = bt.ind.SMA(self.data_1d.close, period=int(self.p.value))
                    elif self.p.interval == '1week':
                        self.sma = bt.ind.SMA(self.data_1w.close, period=int(self.p.value))
                    self.sma_interval = self.p.interval
                    self.sma_weight = self.p.weight
                    self.full_weight += self.sma_weight
                    self.sma_exist = True

                elif self.p.indicator == 'ema':
                    print("Ema created!")
                    if self.p.interval == '15min':
                        self.ema = bt.ind.EMA(self.data_15m.close, period=int(self.p.value))
                    elif self.p.interval == '30min':
                        self.ema = bt.ind.EMA(self.data_30m.close, period=int(self.p.value))
                    elif self.p.interval == '1hour':
                        self.ema = bt.ind.EMA(self.data_1h.close, period=int(self.p.value))
                    elif self.p.interval == '4hours':
                        self.ema = bt.ind.EMA(self.data_4h.close, period=int(self.p.value))
                    elif self.p.interval == '12hours':
                        self.ema = bt.ind.EMA(self.data_12h.close, period=int(self.p.value))
                    elif self.p.interval == '1day':
                        self.ema = bt.ind.EMA(self.data_1d.close, period=int(self.p.value))
                    elif self.p.interval == '1week':
                        self.ema = bt.ind.EMA(self.data_1w.close, period=int(self.p.value))
                    self.ema_interval = self.p.interval
                    self.ema_weight = self.p.weight
                    self.full_weight += self.ema_weight
                    self.ema_exist = True

                elif self.p.indicator == 'rsi' and self.rsi_exist:
                    self.rsi_buy = self.p.value

                elif self.p.indicator == 'rsi':
                    if self.p.interval == '15min':
                        self.rsi = bt.ind.RSI(self.data_15m.close)
                    elif self.p.interval == '30min':
                        self.rsi = bt.ind.RSI(self.data_30m.close)
                    elif self.p.interval == '1hour':
                        self.rsi = bt.ind.RSI(self.data_1h.close)
                    elif self.p.interval == '4hours':
                        self.rsi = bt.ind.RSI(self.data_4h.close)
                    elif self.p.interval == '12hours':
                        self.rsi = bt.ind.RSI(self.data_12h.close)
                    elif self.p.interval == '1day':
                        self.rsi = bt.ind.RSI(self.data_1d.close)
                    elif self.p.interval == '1week':
                        self.rsi = bt.ind.RSI(self.data_1w.close)
                    self.rsi_interval = self.p.interval
                    self.rsi_weight = self.p.weight
                    self.rsi_sell = self.p.value
                    self.full_weight += self.rsi_weight
                    self.rsi_exist = True



        # if self.p.doji:
        #     bt.talib.CDLDOJI(self.data.open, self.data.high,
        #                      self.data.low, self.data.close)

        # elif self.p.ind == 'ema':
        #     bt.talib.EMA(timeperiod=25, plotname='TA_SMA')
        #     bt.indicators.EMA(period=25)
        # elif self.p.ind == 'stoc':
        #     bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
        #                    fastk_period=14, slowk_period=3, slowd_period=3,
        #                    plotname='TA_STOCH')
        #
        #     bt.indicators.Stochastic(self.data)
        #
        # elif self.p.ind == 'macd':
        #     bt.talib.MACD(self.data, plotname='TA_MACD')
        #     bt.indicators.MACD(self.data)
        #     bt.indicators.MACDHisto(self.data)
        # elif self.p.ind == 'bollinger':
        #     bt.talib.BBANDS(self.data, timeperiod=25,
        #                     plotname='TA_BBANDS')
        #     bt.indicators.BollingerBands(self.data, period=25)
        #
        # elif self.p.ind == 'rsi':
        #     bt.talib.RSI(self.data, plotname='TA_RSI')
        #     bt.indicators.RSI(self.data)
        #
        # elif self.p.ind == 'aroon':
        #     bt.talib.AROON(self.data.high, self.data.low, plotname='TA_AROON')
        #     bt.indicators.AroonIndicator(self.data)
        #
        # elif self.p.ind == 'ultimate':
        #     bt.talib.ULTOSC(self.data.high, self.data.low, self.data.close,
        #                     plotname='TA_ULTOSC')
        #     bt.indicators.UltimateOscillator(self.data)
        #
        # elif self.p.ind == 'trix':
        #     bt.talib.TRIX(self.data, timeperiod=25, plotname='TA_TRIX')
        #     bt.indicators.Trix(self.data, period=25)
        #
        # elif self.p.ind == 'adxr':
        #     bt.talib.ADXR(self.data.high, self.data.low, self.data.close,
        #                   plotname='TA_ADXR')
        #     bt.indicators.ADXR(self.data)
        #
        # elif self.p.ind == 'kama':
        #     bt.talib.KAMA(self.data, timeperiod=25, plotname='TA_KAMA')
        #     bt.indicators.KAMA(self.data, period=25)
        #
        # elif self.p.ind == 'dema':
        #     bt.talib.DEMA(self.data, timeperiod=25, plotname='TA_DEMA')
        #     bt.indicators.DEMA(self.data, period=25)
        #
        # elif self.p.ind == 'ppo':
        #     bt.talib.PPO(self.data, plotname='TA_PPO')
        #     bt.indicators.PPO(self.data, _movav=bt.indicators.SMA)
        #
        # elif self.p.ind == 'tema':
        #     bt.talib.TEMA(self.data, timeperiod=25, plotname='TA_TEMA')
        #     bt.indicators.TEMA(self.data, period=25)
        #
        # elif self.p.ind == 'roc':
        #     bt.talib.ROC(self.data, timeperiod=12, plotname='TA_ROC')
        #     bt.talib.ROCP(self.data, timeperiod=12, plotname='TA_ROCP')
        #     bt.talib.ROCR(self.data, timeperiod=12, plotname='TA_ROCR')
        #     bt.talib.ROCR100(self.data, timeperiod=12, plotname='TA_ROCR100')
        #     bt.indicators.ROC(self.data, period=12)
        #     bt.indicators.Momentum(self.data, period=12)
        #     bt.indicators.MomentumOscillator(self.data, period=12)
        #
        # elif self.p.ind == 'williamsr':
        #     bt.talib.WILLR(self.data.high, self.data.low, self.data.close,
        #                    plotname='TA_WILLR')
        #     bt.indicators.WilliamsR(self.data)

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

        weight = 0

        if not self.position:
            if self.sma_exist:
                if self.sma_interval == '15min':
                    if self.data_15m.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '30min':
                    if self.data_30m.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1hour':
                    if self.data_1h.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '4hours':
                    if self.data_4h.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '12hours':
                    if self.data_12h.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1day':
                    if self.data_1d.close > self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1week':
                    if self.data_1w.close > self.sma:
                        weight += self.sma_weight
                        if self.data_1w.close[-1] < self.sma:
                            print(f"BUY {self.data_1w.close[0]}")

            if self.ema_exist:
                if self.ema_interval == '15min':
                    if self.data_15m.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '30min':
                    if self.data_30m.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1hour':
                    if self.data_1h.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '4hours':
                    if self.data_4h.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '12hours':
                    if self.data_12h.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1day':
                    if self.data_1d.close > self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1week':
                    if self.data_1w.close > self.ema:
                        weight += self.ema_weight

            if self.rsi_exist:
                if float(self.rsi_buy) > self.rsi:
                    weight += self.rsi_weight

            if float(weight) > self.full_weight * 0.5:
                self.order = self.buy()

        else:
            if self.sma_exist:
                if self.sma_interval == '15min':
                    if self.data_15m.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '30min':
                    if self.data_30m.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1hour':
                    if self.data_1h.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '4hours':
                    if self.data_4h.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '12hours':
                    if self.data_12h.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1day':
                    if self.data_1d.close < self.sma:
                        weight += self.sma_weight
                elif self.sma_interval == '1week':
                    if self.data_1w.close < self.sma:
                        weight += self.sma_weight

            if self.ema_exist:
                if self.ema_interval == '15min':
                    if self.data_15m.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '30min':
                    if self.data_30m.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1hour':
                    if self.data_1h.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '4hours':
                    if self.data_4h.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '12hours':
                    if self.data_12h.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1day':
                    if self.data_1d.close < self.ema:
                        weight += self.ema_weight
                elif self.ema_interval == '1week':
                    if self.data_1w.close < self.ema:
                        weight += self.ema_weight

            if self.rsi_exist:
                if float(self.rsi_sell) < self.rsi:
                    weight += self.rsi_weight

            if float(weight) > self.full_weight * 0.5:
                self.order = self.sell()
