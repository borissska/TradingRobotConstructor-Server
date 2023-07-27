import datetime as dt
import backtrader as bt
import pandas as pd
from backtrader_binance import BinanceStore


# Торговая система
class StrategySaveOHLCVToDF(bt.Strategy):
    """Сохраняет OHLCV в DF"""
    params = (  # Параметры торговой системы
        ('coin_target', ''),  #
    )

    def __init__(self):
        self.df = {}
        self.df_tf = {}

    def start(self):
        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
            ticker = data._name
            self.df[ticker] = []
            self.df_tf[ticker] = self.broker._store.get_interval(data._timeframe, data._compression)

    def next(self):
        """Приход нового бара тикера"""
        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
            ticker = data._name
            try:
                status = data._state  # 0 - Live data, 1 - History data, 2 - None
                _interval = data.interval
            except Exception as e:
                if data.resampling == 1:
                    status = 22
                    _interval = self.broker._store.get_interval(data._timeframe, data._compression)
                    _interval = f"_{_interval}"
                else:
                    print("Error:", e)

            if status == 1:
                _state = "Resampled Data"
                if status == 1: _state = "False - History data"
                if status == 0: _state = "True - Live data"

                self.df[ticker].append([bt.num2date(data.datetime[0]), data.open[0], data.high[0], data.low[0], data.close[0], data.volume[0]])

                print('{} / {} [{}] - Open: {}, High: {}, Low: {}, Close: {}, Volume: {} - Live: {}'.format(
                    bt.num2date(data.datetime[0]),
                    data._name,
                    _interval,  # таймфрейм тикера
                    data.open[0],
                    data.high[0],
                    data.low[0],
                    data.close[0],
                    data.volume[0],
                    _state,
                ))


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
    if tf == '3d':
        _timeframe = TimeFrame.Days
        interval = 3
    if tf == '1w': _timeframe = TimeFrame.Weeks
    if tf == '1M': _timeframe = TimeFrame.Months
    return _timeframe, interval


def load_data_Binance(tf, store, edge):
    timeframe, interval = get_timeframe(tf, bt.TimeFrame)
    cerebro = bt.Cerebro(quicknotify=True)

    broker = store.getbroker()
    cerebro.setbroker(broker)

    from_date = dt.datetime.utcnow() - dt.timedelta(days=2500)
    data = store.getdata(timeframe=timeframe, compression=interval, dataname=symbol, start_date=from_date,
                         LiveBars=False, sessionend=dt.time(0, 0), rightedged=edge)

    cerebro.adddata(data)
    cerebro.addstrategy(StrategySaveOHLCVToDF, coin_target=coin_target)
    results = cerebro.run()

    df = pd.DataFrame(results[0].df[symbol], columns=["datetime", "open", "high", "low", "close", "volume"])

    df.to_csv(f"D:\candle_data\Binance\{symbol}\{symbol}-{edge}\{symbol}-{tf}.csv", index=False)


if __name__ == '__main__':

    coin_target = 'USDT'
    symbols = ["BNBUSDT", "XRPUSDT", "ADAUSDT", "LTCUSDT", "RSRUSDT", "AVAXUSDT", "FLOWUSDT"]

    store = BinanceStore(
        api_key="NNNN",
        api_secret="NNNN",
        coin_target=coin_target,
        testnet=False)

    for symbol in symbols:
        for edge in ["rightedge", "leftedge"]:
            for tf in ['1w', '3d', '1d', '12h', '4h', '1h', '30m', '15m', '5m', '1m']:
                load_data_Binance(tf=tf, store=store, edge=edge)
