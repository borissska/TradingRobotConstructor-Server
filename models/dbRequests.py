import re
from backtrader_binance import BinanceStore
from markets.bybitConn import Bybit
import models.db
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from strategy.testStrategy import testStrategy


class ServerDB:
    def __init__(self):
        engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost/tickers", echo=True, pool_size=2)
        models.db.create_database(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.store = None

    def checkRegister(self, email):
        results = self.session.query(models.db.User) \
            .filter(models.db.User.email_address == str(email)) \
            .first()

        if results is not None:
            return "Exist"
        else:
            return "Not exist"

    def checkUser(self, login, password):
        results = self.session.query(models.db.User) \
            .filter(models.db.User.user_name == str(login)) \
            .filter(models.db.User.password == str(password)) \
            .first()

        if results is not None:
            return "Exist"
        else:
            return "Not exist"

    def tickerExist(self, ticker):
        results = self.session.query(models.db.Ticker) \
            .filter(models.db.Ticker.ticker_name == str(ticker)) \
            .first()
        if results is not None:
            return True
        else:
            return False

    def getMarketId(self, market_name_id, token_key, token_secret):
        results = self.session.query(models.db.Market) \
            .filter(models.db.Market.market_name_id == str(market_name_id)) \
            .filter(models.db.Market.token_key == str(token_key)) \
            .filter(models.db.Market.token_secret == str(token_secret)) \
            .first()

        if results is None:
            return -1
        else:
            return results.market_id

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
            .filter(models.db.Parameter.parameter_name_id == int(parameter_name_id)) \
            .filter(models.db.Parameter.parameter_value == str(parameter_value)) \
            .first()

        if results is None:
            return -1
        else:
            return results.parameter_id

    def getElementId(self, strategy_id, element_type_id, interval_id, weight):
        results = self.session.query(models.db.Element) \
            .filter(models.db.Element.strategy_id == int(strategy_id)) \
            .filter(models.db.Element.element_type_id == int(element_type_id)) \
            .filter(models.db.Element.interval_id == int(interval_id)) \
            .filter(models.db.Element.weight == int(weight)) \
            .first()

        if results is None:
            return -1
        else:
            return results.element_id

    def getTestId(self, max_loss, profit_per_year, full_profit):
        results = self.session.query(models.db.Test) \
            .filter(models.db.Test.max_loss == float(max_loss)) \
            .filter(models.db.Test.profit_per_year == float(profit_per_year)) \
            .filter(models.db.Test.full_profit == float(full_profit)) \
            .first()

        if results is None:
            return -1
        else:
            return results.test_id

    def getStrategyId(self, user_id, test_id, ticker_id, strategy_name, percent_of_capital, leverage):
        results = self.session.query(models.db.Strategy) \
            .filter(models.db.Strategy.user_id == int(user_id)) \
            .filter(models.db.Strategy.test_id == int(test_id)) \
            .filter(models.db.Strategy.ticker_id == int(ticker_id)) \
            .filter(models.db.Strategy.strategy_name == str(strategy_name)) \
            .filter(models.db.Strategy.percent_of_capital == float(percent_of_capital)) \
            .filter(models.db.Strategy.leverage == int(leverage)) \
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

    def getElementTypeId(self, element_type):
        results = self.session.query(models.db.Type) \
            .filter(models.db.Type.element_type == str(element_type)) \
            .first()

        if results is None:
            return -1
        else:
            return results.element_type_id

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
            .filter(models.db.Strategy.user_id == int(user_id)) \
            .first()

        if results is None:
            return -1
        else:
            return results.strategy_id

    def getAllElementsByStrategyId(self, strategy_id):
        results = self.session.query(models.db.Type.element_type, models.db.Parameter_Name.parameter_name,
                                     models.db.Parameter.parameter_value, models.db.Interval.interval,
                                     models.db.Element.weight) \
            .select_from(models.db.Element) \
            .join(models.db.Element_Parameter) \
            .join(models.db.Parameter) \
            .join(models.db.Type) \
            .join(models.db.Parameter_Name) \
            .join(models.db.Interval) \
            .filter(models.db.Element.strategy_id == int(strategy_id)) \
            .all()

        if results is None:
            return -1
        else:
            print(results)
            return results

    def getStrategiesWithTests(self, login):
        user_id = self.getUserIdByName(login)
        results = self.session.query(models.db.Strategy.strategy_name, models.db.Strategy.profit,
                                     models.db.Strategy.percent_of_capital, models.db.Test.max_loss,
                                     models.db.Test.full_profit, models.db.Test.profit_per_year,
                                     models.db.State.state_name) \
            .select_from(models.db.Strategy) \
            .join(models.db.Test) \
            .join(models.db.State) \
            .filter(models.db.Strategy.user_id == int(user_id)) \
            .all()

        if results is None:
            return -1
        else:
            results = [tuple(row) for row in results]
            print(results)
            return results

    def addNewUser(self, email, login, password):
        user = models.db.User(user_name=login, email_address=email, password=password)
        self.session.add(user)
        self.session.commit()

    def checkMarketData(self, market, key, secret):
        if market == "Bybit":
            self.store = bybit = Bybit(api_key=key, api_secret=secret)
            if bybit.is_exist:
                balance = bybit.getWalletBalance()
                return balance["result"]["balances"][0]["total"]
            else:
                return None

        elif market == "Binance":
            coin_target = 'USDT'

            self.store = BinanceStore(
                api_key="NNNN",
                api_secret="NNNN",
                coin_target=coin_target,
                testnet=False)

            balance = self.store.getbroker().getcash()
            print(balance)
            return balance

        elif market == "":
            pass

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
            strategy_id = int(strategy.strategy_id)
        else:
            strategy_id = -1

        return strategy_id

    def addDisbalanceElement(self, strategy_id, percent, decreasing, weight, interval):
        parameter_percent_name_id = self.getParameterNameId("candle_body_percent")
        parameter_decreasing_name_id = self.getParameterNameId("candle_body_percent")
        element_type_id = self.getElementTypeId("disbalance")
        interval_id = self.getIntervalId(interval=interval)

        if parameter_percent_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_percent_name_id, parameter_value=percent) == -1:
                parameter_percent = models.db.Parameter(parameter_name_id=parameter_percent_name_id,
                                                        parameter_value=percent)
                self.session.add(parameter_percent)
                self.session.commit()

        if parameter_decreasing_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_decreasing_name_id, parameter_value=decreasing) == -1:
                parameter_decreasing = models.db.Parameter(parameter_name_id=parameter_decreasing_name_id,
                                                           parameter_value=decreasing)
                self.session.add(parameter_decreasing)
                self.session.commit()

        if self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id, interval_id=interval_id,
                             weight=weight) == -1:
            element = models.db.Element(strategy_id=strategy_id, element_type_id=element_type_id,
                                        interval_id=interval_id, weight=weight)
            self.session.add(element)
            self.session.commit()

        parameter_percent_id = self.getParameterId(parameter_name_id=parameter_percent_name_id, parameter_value=percent)
        parameter_decreasing_id = self.getParameterId(parameter_name_id=parameter_decreasing_name_id,
                                                      parameter_value=decreasing)
        element_id = self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id,
                                       interval_id=interval_id, weight=weight)

        parameter_percent_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                          parameter_id=parameter_percent_id)
        parameter_decreasing_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                             parameter_id=parameter_decreasing_id)

        self.session.add(parameter_percent_element_parameter)
        self.session.add(parameter_decreasing_element_parameter)
        self.session.commit()

    def addSMAElement(self, strategy_id, period, weight, interval):
        parameter_period_name_id = self.getParameterNameId("period")
        element_type_id = self.getElementTypeId("sma")
        interval_id = self.getIntervalId(interval=interval)

        if parameter_period_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_period_name_id, parameter_value=period) == -1:
                parameter_period = models.db.Parameter(parameter_name_id=parameter_period_name_id,
                                                       parameter_value=period)
                self.session.add(parameter_period)
                self.session.commit()

        if self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id, interval_id=interval_id,
                             weight=weight) == -1:
            element = models.db.Element(strategy_id=strategy_id, element_type_id=element_type_id,
                                        interval_id=interval_id, weight=weight)
            self.session.add(element)
            self.session.commit()

        parameter_period_id = self.getParameterId(parameter_name_id=parameter_period_name_id, parameter_value=period)
        element_id = self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id,
                                       interval_id=interval_id, weight=weight)

        parameter_period_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                         parameter_id=parameter_period_id)

        self.session.add(parameter_period_element_parameter)
        self.session.commit()

    def addEMAElement(self, strategy_id, period, weight, interval):
        parameter_period_name_id = self.getParameterNameId("period")
        element_type_id = self.getElementTypeId("ema")
        interval_id = self.getIntervalId(interval=interval)

        if parameter_period_name_id != -1:
            if self.getParameterId(parameter_name_id=parameter_period_name_id, parameter_value=period) == -1:
                parameter_period = models.db.Parameter(parameter_name_id=parameter_period_name_id,
                                                       parameter_value=period)
                self.session.add(parameter_period)
                self.session.commit()

        if self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id, interval_id=interval_id,
                             weight=weight) == -1:
            element = models.db.Element(strategy_id=strategy_id, element_type_id=element_type_id,
                                        interval_id=interval_id, weight=weight)
            self.session.add(element)
            self.session.commit()

        parameter_period_id = self.getParameterId(parameter_name_id=parameter_period_name_id, parameter_value=period)
        element_id = self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id,
                                       interval_id=interval_id, weight=weight)

        parameter_period_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                         parameter_id=parameter_period_id)

        self.session.add(parameter_period_element_parameter)
        self.session.commit()

    def addRSIElement(self, strategy_id, sell_percent, buy_percent, weight, interval):
        sell_percent_name_id = self.getParameterNameId("sell_percent_rsi")
        buy_percent_name_id = self.getParameterNameId("buy_percent_rsi")
        element_type_id = self.getElementTypeId("rsi")
        interval_id = self.getIntervalId(interval=interval)

        if sell_percent_name_id != -1:
            if self.getParameterId(parameter_name_id=sell_percent_name_id, parameter_value=sell_percent) == -1:
                parameter_sell_percent = models.db.Parameter(parameter_name_id=sell_percent_name_id,
                                                             parameter_value=sell_percent)
                self.session.add(parameter_sell_percent)
                self.session.commit()

        if buy_percent_name_id != -1:
            if self.getParameterId(parameter_name_id=buy_percent_name_id, parameter_value=buy_percent) == -1:
                parameter_buy_percent = models.db.Parameter(parameter_name_id=buy_percent_name_id,
                                                            parameter_value=buy_percent)
                self.session.add(parameter_buy_percent)
                self.session.commit()

        if self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id, interval_id=interval_id,
                             weight=weight) == -1:
            element = models.db.Element(strategy_id=strategy_id, element_type_id=element_type_id,
                                        interval_id=interval_id, weight=weight)
            self.session.add(element)
            self.session.commit()

        sell_percent_name_id = self.getParameterId(parameter_name_id=sell_percent_name_id, parameter_value=sell_percent)
        buy_percent_name_id = self.getParameterId(parameter_name_id=buy_percent_name_id, parameter_value=buy_percent)
        element_id = self.getElementId(strategy_id=strategy_id, element_type_id=element_type_id,
                                       interval_id=interval_id, weight=weight)

        parameter_percent_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                          parameter_id=sell_percent_name_id)
        parameter_decreasing_element_parameter = models.db.Element_Parameter(element_id=element_id,
                                                                             parameter_id=buy_percent_name_id)

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

        test_id, test_time = self.testStrategyPlug()
        strategy_id = self.addStrategy(test_id=test_id, user_name=user_name, strategy_name=strategy_name,
                                       percent_of_capital=percent_of_capital, leverage=leverage,
                                       ticker=ticker)

        if self.tickerExist(ticker):
            for el in list_items:
                str_el = re.split("[ :;()]", str(el))
                element_type = str_el[0]
                if element_type == "Disbalance":
                    percent = str_el[2]
                    decreasing = str_el[5]
                    weight = str_el[8]
                    interval = str_el[11]
                    self.addDisbalanceElement(strategy_id=strategy_id, percent=percent, decreasing=decreasing,
                                              weight=weight, interval=interval)

                elif element_type == "SMA":
                    period = str_el[2]
                    weight = str_el[5]
                    interval = str_el[8]
                    self.addSMAElement(strategy_id=strategy_id, period=period, weight=weight, interval=interval)

                elif element_type == "RSI":
                    sell = str_el[2]
                    buy = str_el[5]
                    weight = str_el[8]
                    interval = str_el[11]
                    self.addRSIElement(strategy_id=strategy_id, sell_percent=sell, buy_percent=buy,
                                       weight=weight, interval=interval)

                elif element_type == "EMA":
                    period = str_el[2]
                    weight = str_el[5]
                    interval = str_el[8]
                    self.addEMAElement(strategy_id=strategy_id, period=period, weight=weight, interval=interval)

        strategy = self.getAllElementsByStrategyId(strategy_id)
        cash = 10000
        commission = 0.001
        max_loss, profit_per_year, full_profit = testStrategy(ticker=ticker, cash=cash,
                                                              percent_of_capital=percent_of_capital,
                                                              strategy=strategy, commission=commission,
                                                              strategy_name=strategy_name, store=self.store)

        self.session.query(models.db.Test) \
            .filter(models.db.Test.test_id == test_id) \
            .filter(models.db.Test.time == test_time) \
            .update({"max_loss": max_loss, "profit_per_year": profit_per_year, "full_profit": full_profit})

    def testStrategyPlug(self, max_loss=0, profit_per_year=0, full_profit=0):
        test = models.db.Test(max_loss=max_loss, profit_per_year=profit_per_year, full_profit=full_profit)
        self.session.add(test)
        self.session.commit()

        return int(test.test_id), test.time