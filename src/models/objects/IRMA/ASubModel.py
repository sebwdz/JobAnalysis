
from .AModel import AModel


class ASubModel(AModel):

    def __init__(self):
        super(ASubModel, self).__init__()
        self._inputs = {}

    def build(self, **kwargs):
        self._build(**kwargs)
