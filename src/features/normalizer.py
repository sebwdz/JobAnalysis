

def simple_min_max(df, columns=None):
    tmp = df if columns is None else df[columns]
    tmp = (tmp - tmp.min()) / (tmp.max() - tmp.min())
    return tmp
