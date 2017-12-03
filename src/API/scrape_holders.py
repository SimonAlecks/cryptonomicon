from time import sleep
from src.API import EtherScanEngine
from src.API.scrape_functions import *
from time import sleep


class EtherHolders(EtherScanEngine):

    # This scraping expects the following schema
    expected_schema = ('Rank', 'Address', 'Quantity', 'Percentage')

    def __init__(self, currency, **kwargs):
        super(self.__class__, self).__init__(currency, **kwargs)

    def run(self, **kwargs):
        data = {}
        for currency, address in self.contract_addresses.items():
            out = self._get_all_holders(address, **kwargs)
            data.update({currency: out})
        return data

    def _get_all_holders(self, address, **kwargs):
        sleep_time = kwargs.get('sleep', 5)

        scraped_data = []
        p = 1
        while True:
            if sleep_time:
                sleep(sleep_time)

            # Define list of dictionaries that parameterize our query,
            # and turn into dictionary.
            query_list = [self.holders_contract_address_query(address), self.page_query(p)]
            params = self._get_requests_params(query_list)

            # Query data
            data_rows = ScrapeMethods.get_webdata(self.holders_url, params)

            # Should we loop again?
            if self._check_for_break(data_rows, p):
                return scraped_data

            scraped_data = self._scrape_data(data_rows, scraped_data)
            p = p + 1
            print("scraping page {0} from url:{1} with params{2}".format(p, self.holders_url, params))

    def _scrape_data(self, rows, scraped_data):
        """ For each page, assert the schema holds, then get the grows"""
        for n, row in enumerate(rows):
            if n == 0:
                cols = ScrapeMethods.get_column(row)
                assert cols == self.expected_schema, "Scraping failed scheme validation"
            else:
                rows = ScrapeMethods.get_data(row)
                scraped_data.append(rows)
        return scraped_data

    def _check_for_break(self, data_rows, p):
        """Every page has 50 rows, except the last page, which has between 1 and 50 rows"""
        if self._end_reached(data_rows):
            return True
        if p == 5:
            return True

    @staticmethod
    def _end_reached(data_rows):
        try:
            check = data_rows[1].find_all('td')[1].text
            if re.findall('There are no matching entries', check.text):
                return True
        except Exception as e:
            return False



