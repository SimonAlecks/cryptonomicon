import re
import requests
from bs4 import BeautifulSoup

""" General methods for use in Etherscan classes"""

class ScrapeMethods:

    @classmethod
    def filter_contract_address(cls, filter_soup):
        line = filter_soup.find_next_sibling("td").text
        filter_value = re.findall("\\n(.*)", line)
        return filter_value[0]

    @classmethod
    def get_webdata(cls, url, params):
        req = requests.get(url, params)
        s = BeautifulSoup(req.text, 'html.parser')
        table = s.find('table', {"class": "table"})
        rows = table.find_all('tr')
        return rows

    @classmethod
    def get_column(cls, row):
        row = tuple(row.text.split())
        return row

    @classmethod
    def get_data(cls, row):
        rows = row.find_all('td')
        parse_rows = tuple(k.text.strip() for k in rows)
        return parse_rows

    @classmethod
    def get_time(cls, row):
        """ parse through rows to find time"""
        rows = row.find_all('td')
        for row in rows:
            if 'title' in str(row):
                return row.find('span')['title']
