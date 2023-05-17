import backtrader as bt


class TestStrategy(bt.Strategy):
    params = (('indicator', 'sma'), ('period', 30),)

    INDS = ['sma', 'ema', 'stoc', 'rsi', 'macd', 'bollinger', 'aroon',
            'ultimate', 'trix', 'kama', 'adxr', 'dema', 'ppo', 'tema',
            'roc', 'williamsr']

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        # if self.p.doji:
        #     bt.talib.CDLDOJI(self.data.open, self.data.high,
        #                      self.data.low, self.data.close)

        if self.p.indicator == 'sma':
            self.sma = bt.indicators.SMA(self.data_close, period=int(self.p.period))

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

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data_close[0] > self.sma[0]:
                self.order = self.buy()
        else:
            if self.data_close[0] < self.sma[0]:
                self.order = self.sell()
