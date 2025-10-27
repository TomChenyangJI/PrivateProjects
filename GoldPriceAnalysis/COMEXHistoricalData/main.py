import json
from datetime import datetime
import pandas as pd

with open('data.json') as fi:
    d = json.load(fi)

quote = d.get("chart").get("result")[0].get("indicators").get("quote")[0]
timeS = d.get("chart").get("result")[0].get("timestamp")

timeS = [datetime.fromtimestamp(e).strftime("%Y-%m-%d") for e in timeS]
open = quote.get('open')
low = quote.get('low')
close = quote.get('close')
volume = quote.get('volume')
head = ('timestamp', 'open', 'low', 'close', 'volume')
data = list(zip(timeS, open, low, close, volume))
# data.reverse()
data.insert(0, head)

# print(list(data))
d = pd.DataFrame(data)
d.to_excel("COMEX_Historical_data.xlsx")
