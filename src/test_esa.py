
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sklearn.linear_model

import data.esa
import features.tools
import features.supervised
import keras


esa, columns = data.esa.data_set()

####
# here, transform data
###
esa = esa.drop("Date", axis=1)

s_data = (esa / esa.sum())
s_data = s_data.transpose()
s_data = (s_data - s_data.min()) / (s_data.max() - s_data.min())
s_data = s_data.transpose()

display = s_data.copy()

input_data, output_data = features.supervised.to_time(s_data, 12, 6, 6)
_, display = features.supervised.to_time(display, 12, 6, 1)

input_f = features.tools.merge_all(input_data)
input_data2 = np.array(list(input_f["features"]))


def baseline_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(300, input_dim=444, kernel_initializer='normal', activation='relu'))
    model.add(keras.layers.Dense(200, input_dim=300, kernel_initializer='normal', activation='relu'))
    model.add(keras.layers.Dense(6, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

result = dict()

for k in output_data.columns.values:
    output_data2 = np.array(list(output_data[k]))

    x_train = input_data2[:40]
    y_train = output_data2[:40]

    xx_train = x_train
    yy_train = y_train

    model = baseline_model()
    model.fit(xx_train, yy_train, batch_size=20, epochs=400, verbose=0)
    y = model.predict(input_data2, batch_size=128)

    last_xx = np.array(list(s_data.tail(40)[k]))
    last_y = y[-1]

    x = [xx for xx in range(0, 40)]
    y = [None for xx in range(0, 40 - 6)] + list(last_y)

    r = sklearn.linear_model.LinearRegression()
    r.fit([[0], [1], [2], [3], [4], [5]], last_y)
    ry = r.predict([[0], [1], [2], [3], [4], [5]])

    result[k] = r.coef_

    ry = [None for xx in range(0, 40 - 6)] + list(ry)

    plt.plot(last_xx)
    plt.plot(ry)
    #plt.scatter(x, y)
    plt.show()

pd.DataFrame(result).to_csv("../data/interim/scores_cesatem.csv")
