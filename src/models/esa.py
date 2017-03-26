
import keras.models
import keras.layers

import models.objects.KerasModel


class Model(models.objects.KerasModel.Model):

    def __init__(self):
        super(Model, self).__init__()

    def build(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(300, input_dim=444, kernel_initializer='normal', activation='relu'))
        model.add(keras.layers.Dense(200, input_dim=300, kernel_initializer='normal', activation='relu'))
        model.add(keras.layers.Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model


class Session(models.objects.KerasModel.Session):

    def __init__(self, model, directory):
        super(Session, self).__init__(model, directory)
        try:
            self._model = keras.models.load_model(directory)
        except:
            self._model = self._model.build()
