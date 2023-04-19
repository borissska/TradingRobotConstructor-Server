import backtrader as bt
import re
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
        is_work = True

        while is_work:
            data = {}

            try:
                data = json.loads(user.recv(1024))
            except Exception as e:
                print(e)
                data = ''
                is_work = False

            if len(data) > 0:

                if data["type"] == "disconnect":
                    user.close()

                elif data["type"] == "check register":
                    message = self.checkRegister(email=data["message"])
                    self.sender(user, "check register", message)

                elif data["type"] == "check user":
                    message = self.checkUser(login=data["message"][0], password=data["message"][1])
                    self.sender(user, "check user", message)

                elif data["type"] == "add new user":
                    self.addNewUser(email=data["message"][0], login=data["message"][1], password=data["message"][2])

                elif data["type"] == "test new strategy":
                    self.testNewStrategy(data=data["message"])

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

    def tickerExist(self, ticker):
        results = self.session.query(models.db.Ticker).filter(models.db.Ticker.ticker_name == str(ticker)).first()
        if results is not None:
            return True
        else:
            return False

    def getIntervalId(self, interval):
        results = self.session.query(models.db.Interval) \
            .filter(models.db.Interval.interval == str(interval)) \
            .first()

        if results is None:
            return -1
        else:
            return results.interval_id

    def getTickerId(self, ticker):
        results = self.session.query(models.db.Ticker) \
            .filter(models.db.Ticker.ticker_name == str(ticker)) \
            .first()

        if results is None:
            return -1
        else:
            return results.ticker_id

    def getParameterId(self, parameter_name_id, parameter_value):
        results = self.session.query(models.db.Parameter) \
            .filter(models.db.Parameter.parameter_name_id == str(parameter_name_id)) \
            .filter(models.db.Parameter.parameter_value == str(parameter_value)) \
            .first()

        if results is None:
            return -1
        else:
            return results.parameter_id

    def getElementId(self, strategy_id, element_type_id, interval_id, weight):
        results = self.session.query(models.db.Element) \
            .filter(models.db.Element.strategy_id == str(strategy_id)) \
            .filter(models.db.Element.element_type_id == str(element_type_id)) \
            .filter(models.db.Element.interval_id == str(interval_id)) \
            .filter(models.db.Element.weight == str(weight)) \
            .first()

        if results is None:
            return -1
        else:
            return results.element_id

    def getTestId(self, max_loss, profit_per_year, full_profit):
        results = self.session.query(models.db.Test) \
            .filter(models.db.Test.max_loss == str(max_loss)) \
            .filter(models.db.Test.profit_per_year == str(profit_per_year)) \
            .filter(models.db.Test.full_profit == str(full_profit)) \
            .first()

        if results is None:
            return -1
        else:
            return results.test_id

    def getStrategyId(self, user_id, test_id, ticker_id, strategy_name, percent_of_capital, leverage):
        results = self.session.query(models.db.Strategy) \
            .filter(models.db.Strategy.user_id == str(user_id)) \
            .filter(models.db.Strategy.test_id == str(test_id)) \
            .filter(models.db.Strategy.ticker_id == str(ticker_id)) \
            .filter(models.db.Strategy.strategy_name == str(strategy_name)) \
            .filter(models.db.Strategy.percent_of_capital == str(percent_of_capital)) \
            .filter(models.db.Strategy.leverage == str(leverage)) \
            .first()

        if results is None:
            return -1
        else:
            return results.strategy_id

    def getParameterNameId(self, parameter_name):
        results = self.session.query(models.db.Parameter_Name) \
            .filter(models.db.Parameter_Name.parameter_name == str(parameter_name)) \
            .first()

        if results is None:
            return -1
        else:
            return results.parameter_name_id

    def getUserIdByName(self, user_name):
        results = self.session.query(models.db.User) \
            .filter(models.db.User.user_name == str(user_name)) \
            .first()

        if results is None:
            return -1
        else:
            return results.user_id

    def getStrategyIdByNameAndUser(self, strategy_name, user_id):
        results = self.session.query(models.db.Strategy) \
            .filter(models.db.Strategy.strategy_name == str(strategy_name)) \
            .filter(models.db.Strategy.user_id == str(user_id)) \
            .first()

        if results is None:
            return -1
        else:
            return results.strategy_id

    def addNewUser(self, email, login, password):
        user = models.db.User(user_name=login, email_address=email, password=password)
        self.session.add(user)
        self.session.commit()

    def addStrategy(self, test_id, user_name, strategy_name, percent_of_capital, leverage, ticker):
        user_id = self.getUserIdByName(user_name)
        ticker_id = self.getTickerId(ticker)

        if self.getStrategyId(user_id=user_id, test_id=test_id, ticker_id=ticker_id, strategy_name=strategy_name,
                              percent_of_capital=percent_of_capital, leverage=leverage) == -1:
            strategy = models.db.Strategy(user_id=user_id, state_id=2, test_id=test_id, ticker_id=ticker_id,
                                          strategy_name=strategy_name, profit=0, percent_of_capital=percent_of_capital,
                                          leverage=leverage)
            self.session.add(strategy)
            self.session.commit()

        strategy_id = self.getStrategyIdByNameAndUser(user_id=user_id, strategy_name=strategy_name)

        return strategy_id

    def addDisbalanceElement(self, strategy_id, percent, decreasing, weight, interval):
        parameter_percent_name_id = self.getParameterNameId("candle_body_percent")
        if parameter_percent_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_percent_name_id, parameter_value=percent) == -1:
                parameter_percent = models.db.Parameter(parameter_name_id=parameter_percent_name_id,
                                                        parameter_value=percent)
                self.session.add(parameter_percent)
                self.session.commit()

        parameter_decreasing_name_id = self.getParameterNameId("candle_body_percent")
        if parameter_decreasing_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_decreasing_name_id, parameter_value=decreasing) == -1:
                parameter_decreasing = models.db.Parameter(parameter_name_id=parameter_decreasing_name_id,
                                                           parameter_value=decreasing)
                self.session.add(parameter_decreasing)
                self.session.commit()

        interval_id = self.getIntervalId(interval=interval)

        if self.getElementId(strategy_id=strategy_id, element_type_id=1, interval_id=interval_id, weight=weight) == -1:
            element = models.db.Element(strategy_id=strategy_id, element_type_id=1,
                                        interval_id=interval_id, weight=weight)
            self.session.add(element)
            self.session.commit()

        parameter_percent_id = self.getParameterId(parameter_name_id=parameter_percent_name_id, parameter_value=percent)
        parameter_decreasing_id = self.getParameterId(parameter_name_id=parameter_decreasing_name_id,
                                                      parameter_value=decreasing)
        element_id = self.getElementId(strategy_id=strategy_id, element_type_id=1,
                                       interval_id=interval_id, weight=weight)

        parameter_percent_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                          parameter_id=parameter_percent_id)
        parameter_decreasing_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                             parameter_id=parameter_decreasing_id)

        self.session.add(parameter_percent_element_parameter)
        self.session.add(parameter_decreasing_element_parameter)
        self.session.commit()

    def testNewStrategy(self, data):
        user_name = data["user_name"]
        ticker = data["ticker"]
        leverage = data["leverage"]
        percent_of_capital = data["percent_of_capital"]
        strategy_name = data["strategy_name"]
        list_items = data["test_strategy"]

        if self.tickerExist(ticker):
            for el in list_items:
                str_el = re.split("[ :;()]", str(el))
                element_type = str_el[0]
                if element_type == "Disbalance":
                    percent = str_el[2]
                    decreasing = str_el[5]
                    weight = str_el[8]
                    interval = str_el[11]
                    test_id = self.testStrategyPlug()
                    strategy_id = self.addStrategy(test_id=test_id, user_name=user_name, strategy_name=strategy_name,
                                                   percent_of_capital=percent_of_capital, leverage=leverage,
                                                   ticker=ticker)
                    self.addDisbalanceElement(strategy_id=strategy_id, percent=percent, decreasing=decreasing,
                                              weight=weight, interval=interval)

                elif True:
                    pass

    def testStrategy(self, ticker, interval):
        cerebro = bt.Cerebro()
        ticker = "BTCUSDT"
        data = bt.feeds.GenericCSVData(dataname=f"D:\candleData\{ticker}\{ticker}-1d.csv",
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

    def testStrategyPlug(self, max_loss=0, profit_per_year=0, full_profit=0):
        if self.getTestId(max_loss=max_loss, profit_per_year=profit_per_year, full_profit=full_profit) == -1:
            test = models.db.Test(max_loss=max_loss, profit_per_year=profit_per_year, full_profit=full_profit)
            self.session.add(test)
            self.session.commit()

        results = self.getTestId(max_loss=max_loss, profit_per_year=profit_per_year, full_profit=full_profit)

        return results


if __name__ == '__main__':
    Server().start_server()
