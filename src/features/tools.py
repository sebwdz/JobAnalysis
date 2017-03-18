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
