import pandas as pd


def temporal_merge(df, period):
    new_data = pd.DataFrame()
    for x in df.columns.values:
        it = 0
        data = []
        while it < len(df[x]):
            v = None
            if it + period < len(df[x]):
                for xx in range(period):
                    v = df[x][it + xx] if v is None else v + df[x][it + xx]
                data.append(v)
            it += 3
        new_data[x] = data
    return new_data


def merge_all(df):
    res = {"features": []}
    for x in df.columns.values:
        for y in range(len(df[x])):
            if y >= len(res["features"]):
                res["features"].append(df[x][y])
            else:
                res["features"][y] = res["features"][y] + df[x][y]
    return pd.DataFrame(res)


def columns_as_rows(df):
    res = {"features": []}
    for x in df.columns.values:
        for y in range(len(df[x])):
            res["features"].append(df[x][y])
    return pd.DataFrame(res)


def to_1d(df):
    res = {}
    for x in df.columns.values:
        res[x] = []
        for y in range(len(df[x])):
            res[x].append(df[x][y][0])
    return pd.DataFrame(res)
