
import matplotlib.pyplot as plt


def temporal(df, columns):
    df.plot.line(x="Date", y=columns)
    plt.show()
