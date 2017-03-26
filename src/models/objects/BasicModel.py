
class Model:

    def __init__(self):
        pass


class Session:

    _model = None
    _directory = None

    def __init__(self, model, directory, **kwargs):
        self._model = model
        self._directory = directory

    def save(self):
        pass

    def fit(self, batch, batch_size, iterations, **kwargs):
        pass

    def evaluate(self, batch, batch_size, **kwargs):
        pass

    def predict(self, batch, batch_size, **kwargs):
        pass
