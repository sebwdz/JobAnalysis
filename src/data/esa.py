
import pandas as pd
from .tools import add_name_to_dataset
from .tools import to_glossary
from .tools import columns_without


def data_set():
    data_frame = pd.read_csv("../data/raw/ESA.tsv", delimiter='\t')
    data_frame = data_frame.dropna(axis=0, how='any').reset_index(drop=True)
    columns = columns_without(data_frame, ["Date"])
    return add_name_to_dataset(data_frame, "ESA", columns=columns)


def glossary(columns):
    data_frame = pd.read_csv("../data/raw/Lexique_ESA.tsv", delimiter='\t')
    return to_glossary(data_frame, columns)
