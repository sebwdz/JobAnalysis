
"""import sys

without = list(sys.modules.keys())

import models

for x in sys.modules.keys():
    if x not in without:
        print(x)"""

import pickle
import re
import pandas as pd


"""class Class:

    son = None

    def my_function(self):
        if self.son is not None:
            self.son.my_function()
        print("hehe")


class Class2:

    son = None

    def my_function(self):
        if self.son is not None:
            self.son.my_function()
        print("hoho")

output = open('data.pkl', 'wb')

f = Class()
f.son = Class2()
f.son.son = Class()
f.my_function()

pickle.dump(f, output)

output.close()

# load

file = open('data.pkl', 'rb')

f2 = pickle.load(file)
f2.my_function()"""


class KpiManager(object):

    _kpis = None

    def __init__(self):
        self._kpis = {}
        self._exec_pipe = {}

    def add(self, name, form):
        exec('self._kpis[name] = lambda v:' 'pd.concat([v, pd.DataFrame({"k_' + name + '": ' + form + '})], axis=1)')

    def call(self, name, pipe):
        return self._kpis[name](pipe)

    def compute(self, exec_pipe, pipe):
        for x in exec_pipe:
            if x not in pipe:
                pipe = kpis.call(x, pipe)
        return pipe


class KpiLoader:

    _kpis = None
    _dependencies = None

    def __init__(self):
        self._kpis = dict()
        self._dependencies = dict()
        self._load()
        self._get_dependencies()

    def _load(self):
        self._kpis["kpi1"] = '((v["d_A"] * v["d_B"].min()) / v["d_B"].max()) + v["d_A"]'
        self._kpis["kpi2"] = 'v["k_kpi1"] * v["d_B"]'
        self._kpis["kpi3"] = 'v["d_A"]'
        self._kpis["kpi4"] = 'v["k_kpi3"] * v["k_kpi2"]'

    def _get_dependencies(self):
        p = re.compile('\[\"[A-Za-z0-9_-]*\"\]')
        for k, x in self._kpis.items():
            ite = p.finditer(x)
            self._dependencies[k] = set()
            for i in ite:
                f, t = i.span()
                self._dependencies[k].add(i.string[f:t][2:-2])

    def fill(self, kpis):
        for k, x in self._kpis.items():
            kpis.add(k, x)




print("loading")
kpis = KpiManager()
loader = KpiLoader()

loader.fill(kpis)

print("get_data")
v1 = pd.DataFrame({"d_A": [2, 3, 10, 4, 40, 40, 20, 1, 4],
                   "d_B": [1, 2, 3, 4, 44, 2, 4, 4, 12]})

print("compute")
res = kpis.compute(["kpi1", "kpi2", "kpi3", "kpi4"], v1)

print(res)
