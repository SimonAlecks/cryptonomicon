import pandas as pd

class Model:

    # Models want training data
    train = pd.DataFrame()

    # Models expect pandas output.
    output = pd.DataFrame()

    def __init__(self):

