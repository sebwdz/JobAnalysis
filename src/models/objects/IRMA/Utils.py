import tensorflow as tf


class Utils:

    @staticmethod
    def new_layer(name, inputs, shape, function):
        with tf.name_scope(name):
            with tf.name_scope("Weights"):
                w = tf.Variable(tf.truncated_normal(shape, stddev=0.1), name="Weight")
            with tf.name_scope("Biases"):
                b = tf.Variable(tf.constant(1.0, shape=[shape[-1]]), name="Biases")
            with tf.name_scope("Pre-activation"):
                pre_activation = tf.matmul(inputs, w, name="Pre-activation") + b
            with tf.name_scope("Activation"):
                return function(pre_activation, name="Activation")
