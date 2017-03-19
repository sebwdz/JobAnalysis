import pandas as pd
from .tools import add_name_to_dataset
from .tools import to_glossary
from .tools import columns_without


def data_set():
    data_frame = pd.read_csv("../data/raw/SNAMPTCSCS.tsv", delimiter='\t')
    data_frame = data_frame.dropna(axis=0, how='any').reset_index(drop=True)
    columns = columns_without(data_frame, ["Date"])
    return add_name_to_dataset(data_frame, "SNAMPTCSCS", columns=columns)


def glossary(columns):
    data_frame = pd.read_csv("../data/raw/Lexique_SNAMPTCSCS.tsv", delimiter='\t')
    return to_glossary(data_frame, columns)
