
from .IModel import IModel


class AModel(IModel):

    _outputs = {}
    _train_op = {}
    _accuracy = {}
    _feeds = {}
    _cost = {}

    def __init__(self):
        super(AModel, self).__init__()
        self._inputs = {}
        self._outputs = {}
        self._cost = {}
        self._train_op = {}
        self._accuracy = {}
        self._feeds = {}

    def add_sub_module(self, module):
        self._feeds = {**self._feeds, **module.get_feeds()}
        self._train_op = {**self._train_op, **module.get_train_op()}
        self._accuracy = {**self._accuracy, **module.get_accuracy()}
        self._outputs = {**self._outputs, **module.get_outputs()}


    def get_outputs(self):
        return self._outputs

    def get_train_op(self):
        return self._train_op

    def get_cost(self):
        return self._cost

    def get_accuracy(self):
        return self._accuracy

    def get_feeds(self):
        return self._feeds

    def _build(self, **kwargs):
        pass
