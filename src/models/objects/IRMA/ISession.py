
class ISession(object):

    def __init__(self):
        super(ISession, self).__init__()

    def fit(self, batch, iteration):
        pass

    def evaluate(self, batch, iteration):
        pass

    def predict(self, batch):
        pass
