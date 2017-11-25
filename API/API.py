import pandas as pd
from datetime import datetime
import requests
from urllib.parse import urlencode
from coinbase.wallet.client import Client
import csv
from urllib.request import urlopen


class PoloniexAPI():
    base_url = 'https://poloniex.com/public?'

    publicMethods = [
        'returnTicker',
        'return24hVolume',
        'returnOrderBook',
        'marketTradeHist',
        'returnChartData',
        'returnCurrencies',
        'returnLoanOrders'
    ]

    privateMethods = [
        'returnBalances',
        'returnCompleteBalances',
        'returnDepositAddresses',
        'generateNewAddress',
        'returnDepositsWithdrawals',
        'returnOpenOrders',
        'returnTradeHistory',
        'returnAvailableAccountBalances',
        'returnTradableBalances',
        'returnOpenLoanOffers',
        'returnOrderTrades',
        'returnActiveLoans',
        'returnLendingHistory',
        'createLoanOffer',
        'cancelLoanOffer',
        'toggleAutoRenew',
        'buy',
        'sell',
        'cancelOrder',
        'moveOrder',
        'withdraw',
        'returnFeeInfo',
        'transferBalance',
        'returnMarginAccountSummary',
        'marginBuy',
        'marginSell',
        'getMarginPosition',
        'closeMarginPosition'
    ]

    def __init__(self):
        pass

    def returnchartdata(self, currency_pair='USDT_ETH', start='2015-12-31', end='2017-12-31', periods=4, **kwargs):

        # External validation info
        valid_times = [300, 900, 1800, 7200, 14400, 86400]

        if periods not in list(map(lambda x: x / (pow(60, 2)), valid_times)):
            raise ValueError("Period not accepted by PoloniexAPI")
        else:
            period = periods * pow(60, 2)

        # Check if pairs exist
        if currency_pair not in self.returnticker():
            raise ValueError("This is not a pairing that eixsts!!")

        # Arg Parsing
        start = self.time_to_unix(start)
        end = self.time_to_unix(end)

        query = {'command': 'returnChartData', 'currencyPair': currency_pair, 'start':start, 'end':end, 'period':period}
        # Generate query

        url = self.base_url + urlencode(query)

        api_json = self.query(url).json()
        return api_json

    def returnticker(self):
        query = {'command': 'returnTicker'}
        url = self.base_url + urlencode(query)
        api_json = self.query(url).json()
        return api_json

    def marketTradeHist(self):
        pass

    def query(self, url):
        return requests.get(url)

    @staticmethod
    def time_to_unix(date):
        d = datetime.strptime(date, '%Y-%m-%d')
        return d.timestamp()

class CoinbaseAPI:

    public_key= 'WVxdyH9CfGmV8ooZ'
    secret_key= 'secret'

    base_url = ''

    def __init__(self):
        self.client = Client(
                 self.public_key,
                 self.secret_key,
                 api_version = 'YYYY-MM-DD')

    def returnaccount(self):
        accounts = self.client.get_accounts()
        return accounts.balance


class EtherScanAPI():

    token = '7DHZUMKWFKEF3QUAJDVS4WEDJ9Y4KBGQP7'

    # Constants
    base_url = 'https://api.etherscan.io/api?'

    def __init__(self):
        pass

    def returntokendata(self):
        query={'action': 'token_supply', 'module': 'stats'}
        query.update({'token_name': 'zrx'})

        url = self.base_url + urlencode(query)

        api_json = self.query(url).json()

    def query(self, url):
        return requests.get(url)


class EtherScanCSV:

    base_url = 'https://etherscan.io/chart/'
    suffix = '?output=csv'

    series = [
        'tx',
        'address',
        'etherpice',
        'marketcap',
        'ethersupplygrowth',
        'pendingtx',
        'ens_register'
    ]

    def __init__(self):
        pass

    def download_series(self, series=None):
        if series not in self.series:
            raise ValueError("Series doesn't exist")

        s = requests.Session()
        url = self.base_url + series + self.suffix
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        df = pd.DataFrame(data=my_list)
        df.columns = df.iloc[0, :]
        df = df.iloc[1:, :]
        df = df.set_index('Date(UTC)')
        return df





