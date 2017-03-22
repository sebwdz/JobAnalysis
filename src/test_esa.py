
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import data.esa
import data.tools
import features.tools
import features.supervised
import models.objects.NewRecursive
import visualization.simple


outputs = ["ESA_BG"]
esa, columns = data.esa.data_set()

####
# here, transform data
###
esa = esa.drop("Date", axis=1)

s_data = (esa / esa.sum())
s_data = s_data.transpose()
s_data = (s_data - s_data.min()) / (s_data.max() - s_data.min()) * 10
s_data = s_data.transpose()


input_data, output_data = features.supervised.to_time(s_data, 12, 4)

# models

m = models.objects.NewRecursive.Model()

inputs_shape = []
for x in columns:
    inputs_shape.append((x, (None, len(input_data[x][0]))))

outputs_shape = []
for x in outputs:
    outputs_shape.append((x + "_out", (None, 1)))

m.build(inputs_shape=inputs_shape, outputs_shape=outputs_shape, learning_rate=0.0001)


# create session

session = models.objects.NewRecursive.Session(m, "./esa.ckpt")
session.save()

plt.ion()
plt.show()

xx = {}
yy = {}
for x in input_data.columns:
    xx[x] = (np.array(list(input_data[x])))
for x in outputs:
    yy[x + "_out"] = np.array(list(output_data[x]))

train = {**xx, **yy}
for k in train:
    train[k] = train[k][:40]


print("running...")
for it in range(10000):
    session.fit(train, it)
    if it % 400 == 0:
        y = session.predict(xx)
        plt.clf()
        plt.plot(features.tools.to_1d(output_data)[outputs[0]])
        plt.plot(y[outputs[0] + "_out"])
        plt.draw()
        plt.pause(0.001)
        print(y[outputs[0] + "_out"])
        print(session.evaluate(train, it))
        session.save()

print("finish")
session.save()
y = session.predict(xx)
plt.clf()
plt.plot(features.tools.to_1d(output_data)[outputs[0]])
plt.plot(y[outputs[0] + "_out"])
plt.show()
input()