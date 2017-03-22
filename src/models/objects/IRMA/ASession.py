
import tensorflow as tf
from .ISession import ISession
from .IModel import IModel


class ASession(ISession):

    _sess = None
    _saver = None
    _writer = None
    _directory = None
    _summary = None
    _model = IModel()

    def __init__(self, model, directory):
        super(ASession, self).__init__()
        self._directory = directory
        self._model = model
        self._sess = tf.InteractiveSession(graph=self._model.get_graph())
        self._sess.run(tf.global_variables_initializer())
        self._summary = tf.summary.merge_all()
        with self._model.get_graph().as_default():
            try:
                self._saver = tf.train.Saver()
                self._saver.restore(self._sess, directory)
            except:
                pass
        self._writer = tf.summary.FileWriter(directory, self._sess.graph)

    def save(self):
        try:
            self._saver.save(self._sess, self._directory)
        except:
            pass

    def fit(self, batch, iteration):
        res = self._sess.run({**self._model.get_train_op(), "summary": self._summary},
                             self._fit_batch(batch))
        self._writer.add_summary(res["summary"], iteration)
        res.pop("summary", None)
        return res

    def _fit_batch(self, batch):
        pass

    def _batch(self, batch):
        pass

    def evaluate(self, batch, iteration):
        un_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        res = self._sess.run({**self._model.get_accuracy(), "summary": self._summary},
                             self._batch(batch),
                             options=un_options, run_metadata=run_metadata)
        self._writer.add_summary(res["summary"], iteration)
        self._writer.add_run_metadata(run_metadata=run_metadata, tag="step:" + str(iteration))
        res.pop("summary", None)
        return res

    def predict(self, batch):
        return self._sess.run(self._model.get_outputs(),
                              self._batch(batch))
