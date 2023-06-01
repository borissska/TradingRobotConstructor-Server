import backtrader as bt
from collections import defaultdict


class TestStrategy(bt.Strategy):

    def __init__(self, params=None):
        self.data_close = self.datas[0].close
        self.full_weight = 0
        self.sma_exist = False
        self.ema_exist = False
        self.rsi_exist = False

        if params is not None:
            for i in range(len(params)):
                el_type, name, value, interval, weight = params[i]
                setattr(self.params, "indicator", el_type)
                setattr(self.params, "name", name)
                setattr(self.params, "value", value)
                setattr(self.params, "interval", interval)
                setattr(self.params, "weight", weight)
                if self.p.indicator == 'sma':
                    self.sma = bt.ind.SMA(self.data_close, period=int(self.p.value))
                    self.sma_interval = self.p.interval
                    self.sma_weight = self.p.weight
                    self.full_weight += self.sma_weight
                    self.sma_exist = True

                elif self.p.indicator == 'ema':
                    self.ema = bt.ind.EMA(period=int(self.p.value))
                    self.ema_interval = self.p.interval
                    self.ema_weight = self.p.weight
                    self.full_weight += self.ema_weight
                    self.ema_exist = True

                elif self.p.indicator == 'rsi' and self.rsi_exist:
                    self.rsi_buy = self.p.value

                elif self.p.indicator == 'rsi':
                    self.rsi = bt.ind.RSI(self.data_close)
                    self.rsi_interval = self.p.interval
                    self.rsi_weight = self.p.weight
                    self.rsi_sell = self.p.value
                    self.full_weight += self.rsi_weight
                    self.rsi_exist = True

        self.order = None
        self.buy_price = None
        self.buy_comm = None

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

    def next(self):
        weight = 0

        if not self.position:
            if self.sma_exist:
                if self.data_close > self.sma:
                    weight += self.sma_weight

            if self.ema_exist:
                if self.data_close > self.ema:
                    weight += self.ema_weight

            if self.rsi_exist:
                if float(self.rsi_buy) > self.rsi:
                    weight += self.rsi_weight

            if float(weight) > self.full_weight * 0.8:
                self.order = self.buy()

        else:
            if self.sma_exist:
                if self.data_close < self.sma:
                    weight += self.sma_weight

            if self.ema_exist:
                if self.data_close < self.ema:
                    weight += self.ema_weight

            if self.rsi_exist:
                if float(self.rsi_sell) < self.rsi:
                    weight += self.rsi_weight

            if float(weight) > self.full_weight * 0.2:
                self.order = self.sell()
