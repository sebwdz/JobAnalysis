import pandas as pd


def simple_min_max(df, columns):
    tmp = df[columns]
    tmp = (tmp - tmp.min()) / (tmp.max() - tmp.min())
    return tmp