
import json
import pandas as pd
import glob

tmp = dict()
files = glob.glob("list_offres/*.json")
for x in files:
    with open(x) as file:
        res = json.load(file)
        print(x)
        for x in res["records"]:
            for k, v in x.items():
                if k not in tmp:
                    tmp[k] = []
                tmp[k].append(v)
pd.DataFrame(tmp).to_csv("list_offre.tsv", sep='\t', encoding='utf-8')
