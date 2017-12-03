import pandas as pd
from API import PoloniexAPI



class dataframewrapper:

    def __init__(self):
        self.api = PoloniexAPI()

    def get_chartdata(self, currency_pair=None, start='2015-12-31', end ='2017-12-31', periods=4):

        json = self.api.returnchartdata(currency_pair=currency_pair, start=start, end=end, periods=periods)
        df = pd.DataFrame.from_records(json)
        df.loc[:,'date'] = pd.to_datetime(df['date'], unit='s')
        df.set_index('date', inplace=True)
        return df

    def get_all_chartdata(self, start='2015-12-31', end='2017-12-31', periods=4, filter=[]):
        tickers = self.api.returnticker()

        # Exclude frozen
        frozen = []
        for k in tickers.keys():
            if (tickers[k]['isFrozen']) == 0:
                frozen.append(k)

        filtered_tickers = []
        for k in tickers:
            if k not in frozen:
                filtered_tickers.append((k))

        for f in filter:
            filtered_tickers = [s for s in filtered_tickers if f in s]

        data_dict = {}
        for t in filtered_tickers:
            df = self.get_chartdata(currency_pair=t, start=start, end=end, periods=periods)
            data_dict.update({t : df})

        # Turn into multi-index
        return pd.concat(data_dict, axis=1)





