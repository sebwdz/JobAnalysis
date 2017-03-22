
class IModel(object):

    def __init__(self):
        super(IModel, self).__init__()

    def build(self, **kwargs):
        pass

    def get_outputs(self):
        pass

    def get_train_op(self):
        pass

    def get_cost(self):
        pass

    def get_accuracy(self):
        pass

    def get_feeds(self):
        pass
