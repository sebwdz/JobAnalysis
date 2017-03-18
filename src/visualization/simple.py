
import matplotlib.pyplot as plt
import seaborn as sns


def temporal(df, columns=None):
    if columns is not None:
        df.plot.line(x="Date", y=columns)
    else:
        df.plot.line(x="Date")
    plt.show()


def bar(df):
    df.plot.bar()
    plt.show()


def linear_regression(df, x, y, size):
    plt.figure(figsize=size)
    sns.regplot(x=x, y=y, data=df)
    plt.show()


def k_means(df, labels):
    plot = [".", ",", ">", "v", "^", "<", "s", "8"]
    color = ["c", "b", "g", "y", "m", "k"]
    for i in range(0, df.shape[0]):
        plt.scatter(df[i, 0], df[i, 1], c=color[labels[i]],
                    marker=plot[labels[i]], s=200)
    plt.show()


def heat_map(df, x, y, size):
    plt.figure(figsize=size)
    sns.heatmap(df, xticklabels=x, yticklabels=y)
    plt.show()
