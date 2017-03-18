
import pandas as pd
from .tools import add_name_to_dataset
from .tools import to_glossary


def without_micro():
    data_frame = pd.read_csv("../data/raw/CESATEM.tsv", delimiter='\t')
    data_frame = data_frame.dropna(axis=1, how='any')
    columns = ["BR", "BS", "BT", "BV", "BW", "BX", "BY", "BZ", "CA", "CB", "CC", "CD"]
    data_frame = data_frame[columns + ["Date"]]
    return add_name_to_dataset(data_frame, "CESATEM", columns)


def glossary(columns):
    data_frame = pd.read_csv("../data/raw/Lexique_CESATEM.tsv", delimiter='\t')
    return to_glossary(data_frame, columns)
