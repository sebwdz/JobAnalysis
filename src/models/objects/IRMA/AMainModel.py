
import tensorflow as tf
from .AModel import AModel


class AMainModel(AModel):

    _graph = None

    def __init__(self):
        super(AModel, self).__init__()
        self._graph = tf.Graph()

    def get_graph(self):
        return self._graph

    def build(self, **kwargs):
        with self._graph.as_default():
            self._build(**kwargs)
