import matplotlib.pyplot as plt
import numpy as np

class Visualization:

    def __init__(self, df, metrics=[]):
        self.df = df
        self.run()
        self.metrics = metrics

    def run(self):

        indx = self.df.index
        fig = plt.figure()
        l = self.metrics.__len__()
        fig, ax_lst = plt.subplots(1, l)

        for n, d in enumerate(self.df.columns):
            data = np.array(self.df.columns[:, d])
            ax_lst[n].plot(data1=data, data2=indx)





