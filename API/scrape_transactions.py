import os
from bs4 import BeautifulSoup
import pandas as pd
from time import gmtime, strftime, sleep
import API
from API.scrape_functions import *
from collections import defaultdict


class EtherTransactions(API.EtherScanEngine):

    def __init__(self, currency, **kwargs):
        super(self.__class__, self).__init__(currency, **kwargs)
        self.kwargs = kwargs

    def get_transactions(self, **kwargs):
        transactions = self._get_all_transactions(**kwargs)
        return transactions

    def _get_new_transactions(self, **kwargs):
        """ Check database to see if we need only some transactions"""
        pass

    def _get_all_transactions(self, **kwargs):
        """ Get all transactions"""
        sleep_time = kwargs.get('sleep', 5)

        scraped_data = []
        p = 1
        while True:

            # Take a nap to prevent timeouts
            if sleep_time:
                sleep(sleep_time)

            # Define list of dictionaries that parameterize our query,
            # and turn into dictionary.
            query_list = [self.transactions_contract_address_query, self.page_query(p)]
            params = self._get_requests_params(query_list)

            # Query data
            data_rows = ScrapeMethods.get_webdata(self.transactions_url, params)

            # Check if we should break for some reason
            if self._check_for_break(data_rows, p):
                return scraped_data

            scraped_data = self._scrape_data(p, data_rows, scraped_data)
            p = p + 1

    def _scrape_data(self, p, rows, scraped_data):
        for n, row in enumerate(rows):
            if p == 1 and n == 0:
                cols = ScrapeMethods.get_column(row)
                scraped_data.append(cols)
            else:
                rows = ScrapeMethods.get_data(row)
                rows = [k for k in rows if k != '']
                scraped_data.append(rows)
        return scraped_data