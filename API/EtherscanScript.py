import re
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
from time import gmtime, strftime, sleep


class EtherscanWebScrape:

    url = 'https://etherscan.io/token'
    token_transactions = '/generic-tokentxns2?'
    token_holders = '/generic-tokenholders2?'
    headers = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, currency):

        self.request = Request('https://etherscan.io/token/{0}#balances'.format(currency),
                               headers=self.headers)
        self.contract_address = self.get_contract_address()
        self.currency = currency

    def get_contract_address(self):
        soup = self._get_main_page()
        filter_soup = soup.find_all('td')
        for n, l in enumerate(filter_soup):
            if re.search(r"Contract", l.text):
                v = self._get_contract_address(l)
                return v

    def _get_main_page(self):
        return BeautifulSoup(urlopen(self.request).read(), 'html.parser')

    @staticmethod
    def _get_contract_address(filter_soup):
        line = filter_soup.find_next_sibling("td").text
        v = re.findall("\\n(.*)", line)
        return v

    @staticmethod
    def _get_webdata(url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        s = BeautifulSoup(urlopen(req).read(), 'html.parser')
        s = s.find('table', {"class": "table"})
        rows = s.find_all('tr')
        return rows

    @staticmethod
    def _get_column(row):
        cols = row.text.split()
        return cols

    @staticmethod
    def _get_data(row):
        cols = row.find_all('td')
        cols = [k.text.strip() for k in cols]
        return cols

