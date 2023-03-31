import backtrader as bt
import strategy
import socket


# sock = socket.socket()
# sock.bind(('', 9090))
# sock.listen(1)
# conn, addr = sock.accept()
#
# print('connected:', addr)
#
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data.upper())
#
# conn.close()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(dataname="D:\candleData\BTCUSDT\BTCUSDT-1d.csv",
                                   separator=',',
                                   dtformat='%Y-%m-%d %H:%M:%S',
                                   timeframe=bt.TimeFrame.Minutes,
                                   openinterest=-1
                                   )
    strats = cerebro.addstrategy(strategy.TestStrategy)
    cerebro.resampledata(data, compression=3600, timeframe=bt.TimeFrame.Minutes)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=5)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='bar')