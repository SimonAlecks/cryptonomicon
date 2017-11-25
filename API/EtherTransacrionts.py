import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
from time import gmtime, strftime, sleep
import API

FLD_CONTRACT_ADDRESS = 'contractAddress'


class EtherTransactions(API.EtherscanWebScrape):

    @property
    def contract_address(self):
        return {FLD_CONTRACT_ADDRESS: self.contract_address[0]}

    def __init__(self, currency, **kwargs):
        super(self.__class__, self).__init__(currency)
        self.kwargs = kwargs
        self.contract_params = {'contractAddress': self.contract_address[0]}

    def get_transactions(self):
        transactions = self._get_all_transactions()
        return transactions

    def _get_all_transactions(self):

        q = urlencode(self.contract_address)

        scraped_data = []
        p = 1
        while True:
            url = self._get_url(p, q)
            sleep(5)
            rows = self._get_webdata(url)

            if len(rows) < 50 or p == 2:
                break

            scraped_data = self._scrape_loop(p, rows, scraped_data)
            print(p)
            p = p + 1

    def _get_url(self, p, q):
        url = self.url + self.token_transactions + q + '&p=' + str(p)
        return url

    #@staticmethod
    #def results_to_dataframe(df):
    #    # Clean data
    #    df = pd.DataFrame(df[1:], columns=df[0])
    #    return df

    def _scrape_loop(self, p, rows, scraped_data):
        for n, row in enumerate(rows):
            if p == 1 and n == 0:
                cols = self._get_column(row)
                scraped_data.append(cols)
            else:
                cols = self._get_data(row)
                cols = [k for k in cols if k != '']
                scraped_data.append(cols)