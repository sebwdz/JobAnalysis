
import pandas as pd


def read_cesatem():
    data_frame = pd.read_csv("../data/raw/CESATEM.tsv", delimiter='\t')
    d1 = data_frame.head(1)
    d2 = data_frame.tail(1)
    data = pd.concat([d1, d2])
    data = data.dropna(axis=1, how='any')
    return data