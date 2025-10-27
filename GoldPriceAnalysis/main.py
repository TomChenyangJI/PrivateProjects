import json
from datetime import datetime

# sh
with open("sh.json", 'r') as fi:
    data = json.load(fi)

zp = data.get('zp')  # morning
wp = data.get('wp')  # afternoon

with open("afternoon_price.txt", "w") as outfi:
    result = ""
    for ele1, ele2 in zip(zp, wp):
        # print(ele1[1] - ele2[1])
        # date
        timestamp = ele2[0] // 1000
        result += str(datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")) + "\t" + str(ele2[1]) + "\n"
    outfi.write(result)


# comex
with open("comex.json", 'r') as fi:
    data = json.load(fi)
    result = ""

for ele in data:
    date = ele.get("date")
    value = ele.get("value")
    result += date + "\t" + value + "\n"
with open("comex.txt", "w") as outfi:
    outfi.write(result)