import json


with open("../professions.bak.2.txt", "r") as infi:
    content = infi.read()

prof_sub_prof_map = {}

mid_li = content.split("\n\n")
for chunk in mid_li:
    prof = chunk.split("*")
    parent_prof = prof[0].strip()
    child_profs = prof[1].strip()
    child_profs = child_profs.split("\n")
    prof_sub_prof_map[parent_prof] = child_profs

print(prof_sub_prof_map)

with open("Relations/parent_child_prof_map.json", "w") as outfi:
    json.dump(prof_sub_prof_map, outfi)

