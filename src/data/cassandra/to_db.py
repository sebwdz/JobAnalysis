import cassandra.cluster
import pandas as pd
import time
import datetime
import sys
import math

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


cluster = cassandra.cluster.Cluster(["127.0.0.1"])
session = cluster.connect()

session.row_factory = pandas_factory
session.default_fetch_size = None

df = pd.read_csv(sys.argv[1], delimiter='\t')
to = sys.argv[2]
glossary = sys.argv[3]
format = sys.argv[4]

columns = df.columns.values
col = "date, "
request = "id uuid, date timestamp, "
for x in columns:
    if x != 'Date':
        col += x + "_, "
        request += "" + x + "_" + " double, "
request = "CREATE TABLE IF NOT EXISTS core.time_series (source TEXT, key TEXT, date TIMESTAMP, value double, PRIMARY KEY ((source, key), date)) WITH CLUSTERING ORDER BY (date ASC)"
col = col[:-2]
session.execute(request)
for x in df:
    request = "BEGIN BATCH "
    if x != 'Date':
        for r in range(len(df[x])):
            if not math.isnan(df[x][r]):
                request += " INSERT INTO core.time_series(source, key, date, value) VALUES("
                if df["Date"][r][0] != "T":
                    date = time.mktime(datetime.datetime.strptime(df["Date"][r], "%m/%Y").timetuple())
                else:
                    date = str(((int(df["Date"][r][1]) - 1) * 3 + 1)) + df["Date"][r][2:]
                    date = time.mktime(datetime.datetime.strptime(date, "%m/%Y").timetuple())
                date = datetime.datetime.fromtimestamp(
                    int(date)
                ).strftime('%Y-%m-%d %H:%M:%S GMT')
                request += "'" + to + "', '" + x + "', '" + date + "', " + str(df[x][r])
                request += ");"
        request += "APPLY BATCH"
        session.execute(request)

result = session.execute("SELECT key, min(date), max(date) FROM core.time_series WHERE source = '" + to + "' GROUP BY key ALLOW FILTERING")
print(result._current_rows)
cluster.shutdown()
