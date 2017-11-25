import re
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
from time import gmtime, strftime, sleep
import API

class EtherHolders(API.EtherscanWebScrape):

    def __init__(self, currency):
        super(self.__class__, self).__init__(currency)

    def run(self):
        df = self.get_token_holders()
        self.write_out(df)

    def get_token_holders(self):
        query = {'a': self.contract_address}
        q = urlencode(query)

        scraped_data = []
        p = 1
        while True:
            url = self.url + self.token_holders + q + '&p=' + str(p)
            sleep(5)
            rows = self._get_webdata(url)
            if len(rows) < 50 or p == 20:
                break
            for n, row in enumerate(rows):
                if p == 1 and n == 0:
                    cols = self._get_column(row)
                    scraped_data.append(cols)
                else:
                    cols = self._get_data(row)
                    scraped_data.append(cols)
            print(p)
            p = p + 1

        df = self.results_to_dataframe(scraped_data)
        return df

    def write_out(self, df):
        df.to_csv('{0}\\{1}'.format(os.path.expanduser("~"), 'directory\\test.csv'))

    @staticmethod
    def results_to_dataframe(df):
        # Clean data
        df = pd.DataFrame(df[1:], columns=df[0])

        # Type Handling
        df.loc[:, 'Percentage'] = df.loc[:, 'Percentage'].replace('%', '', regex=True).astype('float')
        df.set_index('Rank', inplace=True)
        df['time'] = strftime("%Y-%m-%d %H:%M", gmtime())

        return df
