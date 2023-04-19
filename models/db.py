import datetime

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

database = declarative_base()


class User(database):
    __tablename__ = "user"

    user_id = sql.Column("user_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    user_name = sql.Column("user_name", sql.String(16), nullable=False)
    email_address = sql.Column("email_address", sql.String(20), nullable=False)
    password = sql.Column("password", sql.String(16), nullable=False)

    def __init__(self, user_name, email_address, password):
        self.user_name = user_name
        self.email_address = email_address
        self.password = password


class Market_Name(database):
    __tablename__ = "market_name"

    market_name_id = sql.Column("market_name_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    market_name = sql.Column("market_name", sql.String(30), nullable=False)

    def __init__(self, market_name):
        self.market_name = market_name


class Market(database):
    __tablename__ = "market"

    market_id = sql.Column("market_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    market_name_id = sql.Column("market_name_id", sql.Integer, sql.ForeignKey("market_name.market_name_id"),
                                nullable=False)
    token_key = sql.Column("token_key", sql.String(50), nullable=False)
    token_secret = sql.Column("token_secret", sql.String(50), nullable=False)

    def __init__(self, market_name_id, token_key, token_secret):
        self.market_name_id = market_name_id
        self.token_key = token_key
        self.token_secret = token_secret


class User_Market(database):
    __tablename__ = "user_market"

    user_market_id = sql.Column("user_market_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    user_id = sql.Column("user_id", sql.Integer, sql.ForeignKey("user.user_id"), nullable=False)
    market_id = sql.Column("market_id", sql.Integer, sql.ForeignKey("market.market_id"), nullable=False)
    capital = sql.Column("capital", sql.Integer)

    def __init__(self, user_id, market_id, capital):
        self.user_id = user_id
        self.market_id = market_id
        self.capital = capital


class Test(database):
    __tablename__ = "test"

    test_id = sql.Column("test_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    max_loss = sql.Column("max_loss", sql.Float, nullable=False)
    profit_per_year = sql.Column("profit_per_year", sql.Float, nullable=False)
    full_profit = sql.Column("full_profit", sql.Float, nullable=False)
    time = sql.Column("time", sql.DateTime, nullable=False, server_default=sql.sql.expression.func.now())

    def __init__(self, max_loss, profit_per_year, full_profit):
        self.max_loss = max_loss
        self.profit_per_year = profit_per_year
        self.full_profit = full_profit


class Ticker(database):
    __tablename__ = "ticker"

    ticker_id = sql.Column("ticker_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    ticker_name = sql.Column("ticker_name", sql.String(8), nullable=False)

    def __init__(self, ticker_name):
        self.ticker_name = ticker_name


class State(database):
    __tablename__ = "state"

    state_id = sql.Column("state_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    state_name = sql.Column("state_name", sql.String(15), nullable=False)
    state_description = sql.Column("state_description", sql.String(1000))

    def __init__(self, state_name, state_description):
        self.state_name = state_name
        self.state_description = state_description


class Interval(database):
    __tablename__ = "interval"

    interval_id = sql.Column("interval_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    interval = sql.Column("interval", sql.String(7), nullable=False)

    def __init__(self, interval):
        self.interval = interval


class Type(database):
    __tablename__ = "element_type"

    element_type_id = sql.Column("element_type_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    element_type = sql.Column("element_type", sql.String(20), nullable=False)

    def __init__(self, element_type):
        self.element_type = element_type


class Element(database):
    __tablename__ = "element"

    element_id = sql.Column("element_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    strategy_id = sql.Column("strategy_id", sql.Integer, sql.ForeignKey("strategy.strategy_id"), nullable=False)
    element_type_id = sql.Column("element_type_id", sql.Integer, sql.ForeignKey("element_type.element_type_id"),
                                 nullable=False)
    interval_id = sql.Column("interval_id", sql.Integer, sql.ForeignKey("interval.interval_id"), nullable=False)
    weight = sql.Column("weight", sql.Integer, nullable=False)

    def __init__(self, strategy_id, element_type_id, interval_id, weight):
        self.strategy_id = strategy_id
        self.element_type_id = element_type_id
        self.interval_id = interval_id
        self.weight = weight


class Parameter_Name(database):
    __tablename__ = "parameter_name"

    parameter_name_id = sql.Column("parameter_name_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    parameter_name = sql.Column("parameter_name", sql.String(20), nullable=False)

    def __init__(self, parameter_name):
        self.parameter_name = parameter_name


class Parameter(database):
    __tablename__ = "parameter"

    parameter_id = sql.Column("parameter_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    parameter_name_id = sql.Column("parameter_name_id", sql.Integer, sql.ForeignKey("parameter_name.parameter_name_id"),
                                   nullable=False)
    parameter_value = sql.Column("parameter_value", sql.String(20), nullable=False)

    def __init__(self, parameter_name_id, parameter_value):
        self.parameter_name_id = parameter_name_id
        self.parameter_value = parameter_value


class Element_Parameter(database):
    __tablename__ = "element_parameter"

    element_parameter_id = sql.Column("element_parameter_id", sql.Integer, index=True, autoincrement=True,
                                      primary_key=True)
    element_id = sql.Column("element_id", sql.Integer, sql.ForeignKey("element.element_id"), nullable=False)
    parameter_id = sql.Column("parameter_id", sql.Integer, sql.ForeignKey("parameter.parameter_id"), nullable=False)

    def __init__(self, element_id, parameter_id):
        self.element_id = element_id
        self.parameter_id = parameter_id


class Strategy(database):
    __tablename__ = "strategy"

    strategy_id = sql.Column("strategy_id", sql.Integer, index=True, autoincrement=True, primary_key=True)
    user_id = sql.Column("user_id", sql.Integer, sql.ForeignKey("user.user_id"), nullable=False)
    state_id = sql.Column("state_id", sql.Integer, sql.ForeignKey("state.state_id"), nullable=False)
    test_id = sql.Column("test_id", sql.Integer, sql.ForeignKey("test.test_id"), nullable=False)
    ticker_id = sql.Column("ticker_id", sql.Integer, sql.ForeignKey("ticker.ticker_id"), nullable=False)
    strategy_name = sql.Column("strategy_name", sql.String(20), nullable=False)
    profit = sql.Column("profit", sql.Float)
    percent_of_capital = sql.Column("percent_of_capital", sql.Float, nullable=False)
    leverage = sql.Column("leverage", sql.Integer, nullable=False)

    def __init__(self, user_id, state_id, test_id, ticker_id, strategy_name, profit, percent_of_capital, leverage):
        self.user_id = user_id
        self.state_id = state_id
        self.test_id = test_id
        self.ticker_id = ticker_id
        self.strategy_name = strategy_name
        self.profit = profit
        self.percent_of_capital = percent_of_capital
        self.leverage = leverage


def create_database(engine):
    database.metadata.create_all(bind=engine)
