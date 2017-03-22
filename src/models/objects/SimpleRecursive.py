import tensorflow as tf
from .IRMA import AMainModel
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


class SubModel(ASubModel):

    _shape_in = None
    _shape_out = None
    _name = None

    def __init__(self, name, shape_in, shape_out):
        super(SubModel, self).__init__()
        self._shape_in = shape_in
        self._shape_out = shape_out
        self._name = name

    # to be moved to utils
    def _new_layer(self, name, inputs, shape, function):
        with tf.name_scope(name):
            with tf.name_scope("Weights"):
                w = tf.Variable(tf.truncated_normal(shape, stddev=0.1), name="Weight")
            with tf.name_scope("Biases"):
                b = tf.Variable(tf.constant(1.0, shape=[shape[-1]]), name="Biases")
            with tf.name_scope("Pre-activation"):
                pre_activation = tf.matmul(inputs, w, name="Pre-activation") + b
            with tf.name_scope("Activation"):
                return function(pre_activation, name="Activation")

    def _build(self, k, name, inputs, learning_rate, intermediate, keep_prop):
        self._feeds = dict({name: tf.placeholder(tf.float32, (None, len(intermediate)), name=name + "_feeds")})
        with tf.name_scope(self._name):
            layer = self._new_layer("Hidden", inputs[0], (int(inputs[0].get_shape()[1]), 50), tf.nn.relu)
            layer = self._new_layer("Hidden", inputs[0], (int(inputs[0].get_shape()[1]), 50), tf.nn.relu)
            layer = tf.nn.dropout(layer, keep_prop)
            self._outputs[name] = self._new_layer(name, layer, (50, len(intermediate)), tf.identity)
            with tf.name_scope("Cost"):
                self._cost[name] = tf.reduce_mean(tf.square(self._outputs[name] - self._feeds[name]), name="Cost")
                tf.summary.scalar('Cost', self._cost[name])
            with tf.name_scope("Accuracy"):
                self._accuracy[name] = tf.reduce_mean(tf.abs(self._outputs[name] - self._feeds[name]), name="Accuracy")
                tf.summary.scalar('Accuracy', self._accuracy[name])
        with tf.name_scope("Optimiser_" + k):
            optimizer = tf.train.AdamOptimizer(learning_rate, name="Optimiser_" + k).minimize(self._cost[name])
        self._train_op[name] = optimizer


class Model(AMainModel):

    def __init__(self):
        super(Model, self).__init__()

    def _build(self, learning_rate, inputs_shape, outputs_shape, intermediate):
        self._feeds = dict({x[0]: tf.placeholder(tf.float32, x[1], name=x[0] + "_feeds") for x in inputs_shape})
        self._feeds["keep_prop"] = tf.placeholder(tf.float32, name="keep_prop")

        sub = {}
        for x in inputs_shape:
            sub[x[0]] = SubModel(x[0], tuple(x[1][1:]), tuple([1]))
            sub[x[0]].build(inputs=[self._feeds[x[0]]], intermediate=intermediate, learning_rate=learning_rate,
                            name=x[0] + "_next", k=x[0], keep_prop=self._feeds["keep_prop"])
            self.add_sub_module(sub[x[0]])

        for x in inputs_shape:
            print(sub[x[0]].get_outputs()[x[0] + "_next"])

        with tf.name_scope("concat"):
            concat = tf.concat([sub[x[0]].get_outputs()[x[0] + "_next"] for x in inputs_shape], 1, name="Concat")

        for x in outputs_shape:
            k = x[0] + "_out"
            sub_final = SubModel(k, tuple([len(sub)]), x[1][1:])
            sub_final.build(inputs=[concat], intermediate=intermediate, learning_rate=learning_rate,
                            name=k + "_next", k=k, keep_prop=self._feeds["keep_prop"])
            self.add_sub_module(sub_final)
