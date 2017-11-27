from API.scrape_functions import *
import re
import requests
from bs4 import BeautifulSoup

FLD_CONTRACT_ADDRESS = 'contractAddress'
FLD_CONTRACT_ADDRESS_HOLDERS = 'a'
FLD_PAGE = 'p'

class EtherScanEngine:

    # Etherscan URL
    url = 'https://etherscan.io'

    # Token transactions
    token_list = '/token'
    token_balance = '/token/{0}#balances'
    token_transactions = '/token/generic-tokentxns2?'
    token_holders = '/token/generic-tokenholders2?'

    # All currencies have a contract address
    contract_addresses = {}

    def __init__(self, currency, **kwargs):
        """ Initialization will get the contract address for the currency string"""

        # Check type, force to be list.
        currency = [currency] if isinstance(currency, str) else currency

        # Iterate over and create dictionary of currency:address
        for c in currency:
            currency_page_request = requests.get('https://etherscan.io/' + self.token_balance.format(c))
            contract_address = self.get_contract_address(currency_page_request)
            self.contract_addresses.update({c: contract_address})

    def _get_currency_page(self, currency_page_request):
        """ read the main page"""
        return BeautifulSoup(currency_page_request.text, 'html.parser')

    def get_contract_address(self, currency_page_request):
        main_page = self._get_currency_page(currency_page_request)
        filter_soup = main_page.find_all('td')
        for l in filter_soup:
            if re.search(r"Contract", l.text):
                v = ScrapeMethods.filter_contract_address(l)
                return v

    def transactions_contract_address_query(self, address):
        return {FLD_CONTRACT_ADDRESS: address}

    def holders_contract_address_query(self, address):
        return {FLD_CONTRACT_ADDRESS_HOLDERS: address}

    def page_query(self, pageno):
        return {FLD_PAGE: pageno}

    def _get_requests_params(self, params):
        new_params = dict()
        for d in params:
            new_params.update(d)
        return new_params

    def _check_for_break(self, data_rows, p):
        #TODO: this isn't solved. edge case when 50
        if len(data_rows) < 50 or p == 2:
            return True

    @property
    def transactions_url(self):
        return self.url + self.token_transactions

    @property
    def holders_url(self):
        return self.url + self.token_holders