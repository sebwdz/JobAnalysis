import pandas as pd


def to_time(df, fr, to):
    rff = {}
    rtf = {}
    for x in df:
        i = 0
        while i + to + fr < len(df[x]):
            if x not in rff:
                rff[x] = []
                rtf[x] = []
            rff[x].append(list(df[x][i:i + fr]))
            rtf[x].append([df[x][fr + to + i]])
            i += 1
    return pd.DataFrame(rff), pd.DataFrame(rtf)
