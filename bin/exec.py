from API import PoloniexAPI
from data import *
from Filter import Kalman
import numpy as np



obj = dataframewrapper()


df = obj.get_all_chartdata()



x_h = np.array(1)
s = np.array(1)
G = np.array(1)
R = np.array(1000)
A = np.array(1)
Q = np.array(1000)

kal = Kalman(df.loc[:,'close'], x_h, s, G, R, A, Q)
p = kal.run()

print(1)