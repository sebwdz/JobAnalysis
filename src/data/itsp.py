import pandas as pd
from .tools import add_name_to_dataset
from .tools import to_glossary
from .tools import columns_without


def data_set():
    data_frame = pd.read_csv("../data/raw/ITSP.tsv", delimiter='\t')
    data_frame = data_frame.dropna(axis=0, how='any').reset_index(drop=True)
    columns = ["CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ",
               "CK", "CL", "CM", "CN", "CO", "CP", "CQ", "CR", "CS", "CT", "CU", "CV", "CW", "CX"]
    data_frame = data_frame[columns + ["Date"]]
    return add_name_to_dataset(data_frame, "ITSP", columns=columns)


def glossary(columns):
    data_frame = pd.read_csv("../data/raw/Lexique_ITSP.tsv", delimiter='\t')
    return to_glossary(data_frame, columns)
