
import models.objects.BasicModel


class Model(models.objects.BasicModel.Model):

    def __init__(self):
        pass

    def build(self, **kwargs):
        pass


class Session(models.objects.BasicModel.Session):

    def __init__(self, model, directory, **kwargs):
        super(Session, self).__init__(model, directory)

    def save(self):
        self._model.save(self._directory)

    def fit(self, batch, batch_size, iterations, **kwargs):
        self._model.fit(batch["xx"], batch["yy"], iterations=iterations, batch_size=batch_size, verbose=0)

    def evaluate(self, batch, batch_size, **kwargs):
        return self._model.evaluate(batch, batch_size=batch_size)

    def predict(self, batch, batch_size, **kwargs):
        return self._model.predict(batch, batch_size=batch_size)


"""def generate_arrays_from_file(path):
    while 1:
        f = open(path)
        for line in f:
            # create numpy arrays of input data
            # and labels, from each line in the file
            x, y = process_line(line)
            img = load_images(x)
            yield (img, y)
        f.close()

model.fit_generator(generate_arrays_from_file('/my_file.txt'),
        samples_per_epoch=10000, nb_epoch=10)"""