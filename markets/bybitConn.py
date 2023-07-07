from enum import Enum
from pybit.unified_trading import HTTP
from pybit.exceptions import FailedRequestError


class Bybit():

    def __init__(self, api_key, api_secret):
        try:
            self.session_auth = HTTP(
                api_key=api_key,
                api_secret=api_secret,
            )
            self.is_exist = True
        except Exception(FailedRequestError):
            self.is_exist = False

    def getWalletBalance(self):
        balance = self.session_auth.get_wallet_balance(accountType="UNIFIED")
        return balance

    # Символ желательно провеять не здесь
    def place_order(self, category, symbol, side, orderType, qty):
        if category in ['spot', 'linear', 'inverse']:
            if side in ['Buy', 'Sell']:
                if orderType in ['Market', 'Limit']:
                    self.session_auth.place_order(category=category,
                                                  symbol=symbol,
                                                  side=side,
                                                  orderType=orderType,
                                                  qty=qty, )
                    return "Done"
                else:
                    return "Error: Order type"
            else:
                return "Error: Side"
        else:
            return "Error: Category"
