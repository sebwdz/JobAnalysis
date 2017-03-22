import tensorflow as tf
from .IRMA import AMainModel
from .IRMA.Utils import Utils
from .IRMA import ASubModel
from .IRMA import ASession


class Session(ASession):

    def __init__(self, model, directory):
        super(Session, self).__init__(model, directory)

    def _fit_batch(self, batch):
        return {**{self._model.get_feeds()[k]: x for k, x in batch.items()},
                self._model.get_feeds()["keep_prop"]: 0.5}

    def _batch(self, batch):
        return {**{self._model.get_feeds()[k]: x for k, x in batch.items()},
                self._model.get_feeds()["keep_prop"]: 1}


class FirstLayerModel(ASubModel):

    def __init__(self):
        super(ASubModel, self).__init__()

    def _build(self, name, shape, feeds):
        with tf.name_scope(name):
            sublayer = feeds[name]
            self._outputs[name] = Utils.new_layer("Hidden", sublayer, (int(sublayer.get_shape()[1]), shape[1]),
                                                  tf.nn.relu)


class SecondLayerModel(ASubModel):

    def __init__(self):
        super(ASubModel, self).__init__()

    def _build(self, name, shape, feeds, layer, learning_rate,):
        with tf.name_scope(name):
            layer = Utils.new_layer("Hidden", layer, (int(layer.get_shape()[1]), 50), tf.nn.relu)
            sublayer = tf.nn.dropout(layer, feeds["keep_prop"])
            self._outputs[name] = Utils.new_layer("Hidden", sublayer, (int(sublayer.get_shape()[1]), shape[1]),
                                                  tf.nn.relu)
            with tf.name_scope("Cost"):
                self._cost[name] = tf.reduce_mean(tf.sqrt(tf.nn.l2_loss(self._outputs[name] - feeds[name])))
                tf.summary.scalar('Cost', self._cost[name])
            with tf.name_scope("Accuracy"):
                self._accuracy[name] = tf.reduce_mean(tf.abs(self._outputs[name] - feeds[name]),
                                                      name="Accuracy") / 10
                tf.summary.scalar('Accuracy', self._accuracy[name])
        with tf.name_scope("Optimiser_" + name):
            optimizer = tf.train.AdamOptimizer(learning_rate, name="Optimiser_" + name).minimize(self._cost[name])
        self._train_op[name] = optimizer


class Model(AMainModel):

    def __init__(self):
        super(Model, self).__init__()

    def _build(self, inputs_shape, outputs_shape, learning_rate):
        self._feeds = dict({x[0]: tf.placeholder(tf.float32, x[1], name=x[0] + "_feeds")
                            for x in inputs_shape + outputs_shape})
        self._feeds["keep_prop"] = tf.placeholder(tf.float32, name="keep_prop")

        with tf.name_scope("Layers"):
            for x in inputs_shape:
                model = FirstLayerModel()
                model.build(name=x[0], shape=(None, 30), feeds=self._feeds)
                self.add_sub_module(model)

        with tf.name_scope("Concat_feeds"):
            inputs_feeds = tf.concat([self._feeds[x[0]] for x in inputs_shape], 1)

        layer = Utils.new_layer("Hidden", inputs_feeds, (int(inputs_feeds.get_shape()[1]), 30), tf.nn.relu)

        with tf.name_scope("Concat_layers"):
            inputs = tf.concat([self._outputs[x[0]] for x in inputs_shape], 1)

        with tf.name_scope("Concat_all"):
            layer = tf.concat([layer, inputs], 1)

        for x in outputs_shape:

            model = SecondLayerModel()
            model.build(name=x[0], shape=x[1], feeds=self._feeds, layer=layer, learning_rate=learning_rate)
            self.add_sub_module(model)