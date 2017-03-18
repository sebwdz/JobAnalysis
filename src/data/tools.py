import numpy as np


def add_name_to_dataset(df, name, columns):
    df.rename(columns=lambda x: name + "_" + x if x in columns else x, inplace=True)
    for x in range(len(columns)):
        columns[x] = name + "_" + columns[x]
    return df, columns


def to_glossary(data_frame, columns):
    data_frame = data_frame.transpose()
    new_header = data_frame.iloc[0]
    data_frame = data_frame[1:]
    data_frame = data_frame.rename(columns=new_header)
    return data_frame[columns]


def columns_without(df, without):
    columns = df.columns.values
    for x in without:
        columns = np.delete(columns, np.where(columns == x))
    return columns
