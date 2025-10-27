import json


with open("7.json", "r") as infi:
    con1 = json.load(infi)

with open("8.json", "r") as infi:
    con2 = json.load(infi)

print(con1 == con2)
print(len(con1))
print(len(con2))