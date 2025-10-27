import json


def reader(obj):
    if type(obj) is list:
        for ele in obj:
            reader(ele)
    elif type(obj) is dict:
        for key, val in obj.items():
            print(key, val)
    else:
        print(obj)


with open("./test.json", "r") as fi:
    # contend = fi.read()
    obj = json.load(fi)
    reader(obj)
