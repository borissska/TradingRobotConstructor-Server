from pybit.spot import HTTP
from pybit.exceptions import FailedRequestError


class Bybit():

    def __init__(self, api_key, api_secret):
        try:
            self.session = HTTP(
                api_key=api_key,
                api_secret=api_secret,
            )
            self.is_exist = True
        except Exception(FailedRequestError):
            self.is_exist = False

    def getWalletBalance(self):
        balance = self.session.get_wallet_balance(accountType="UNIFIED")
        return balance
