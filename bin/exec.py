from API import PoloniexAPI
from data import *
from Filter import Kalman
import numpy as np
from API import *

adj = EtherTransactions(currency='OmiseGo')
adj.get_transactions()

print(1)