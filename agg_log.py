import os
import pandas as pd

csv = [x for x in os.listdir() if x[-3:] == 'csv']
res = []
for x in csv:
    res.append(pd.read_csv(x))
df = pd.concat(res)
df.to_csv('logs.csv', index=False, encoding='utf-8')