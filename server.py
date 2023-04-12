import backtrader as bt
import strategy
from socket import *
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models.db


class Server:
    def __init__(self):
        engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost/tickers", echo=True, pool_size=2)
        models.db.create_database(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('localhost', 9091))
        self.sock.listen(3)

    def start_server(self):
        while True:
            user, addr = self.sock.accept()
            print(f"Client connected:\nIP:{addr[0]}\nPORT:{addr[1]}")
            self.listener(user)

    def sender(self, user, message_type, message):
        message = {"type": message_type, "message": message}
        user.send(json.dumps(message).encode('utf-8'))

    def listener(self, user):
        # self.sender(user, "message", "You are connected!")
        is_work = True

        while is_work:
            data = {}

            try:
                data = json.loads(user.recv(1024))
                # self.sender(user, "message", "Got it!")
            except Exception as e:
                print(e)
                data = ''
                is_work = False

            if len(data) > 0:

                if data["type"] == "disconnect":
                    user.close()
                    is_work = False

                elif data["type"] == "check register":
                    message = self.checkRegister(email=data["message"])
                    self.sender(user, "check register", message)

                elif data["type"] == "check user":
                    message = self.checkUser(login=data["message"][0], password=data["message"][1])
                    self.sender(user, "check user", message)

                elif data["type"] == "add new user":
                    self.addNewUser(email=data["message"][0], login=data["message"][1], password=data["message"][2])

                elif True:
                    pass

                data = ""

            else:
                print("Disconnected")
                is_work = False

    def checkRegister(self, email):
        results = self.session.query(models.db.User)\
            .filter(models.db.User.email_address == str(email))\
            .first()

        if results is not None:
            return "Exist"
        else:
            return "Not exist"

    def checkUser(self, login, password):
        results = self.session.query(models.db.User)\
            .filter(models.db.User.user_name == str(login))\
            .filter(models.db.User.password == str(password))\
            .first()

        if results is not None:
            return "Exist"
        else:
            return "Not exist"

    def addNewUser(self, email, login, password):
        user = models.db.User(user_name=login, email_address=email, password=password)
        self.session.add(user)
        self.session.commit()


async def run_test():
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(dataname="D:\candleData\BTCUSDT\BTCUSDT-1d.csv",
                                   separator=',',
                                   dtformat='%Y-%m-%d %H:%M:%S',
                                   timeframe=bt.TimeFrame.Minutes,
                                   openinterest=-1
                                   )
    cerebro.addstrategy(strategy.TestStrategy)
    cerebro.resampledata(data, compression=3600, timeframe=bt.TimeFrame.Minutes)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=5)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='bar')


def run_server():
    sock = socket()
    sock.bind(('', 9091))
    sock.listen(2)
    conn, addr = sock.accept()

    print('connected:', addr)


if __name__ == '__main__':
    Server().start_server()
