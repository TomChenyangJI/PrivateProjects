

def get_name(p):
    with open(p, "r") as fi:
        lines = fi.readlines()
    for line in lines:
        if "大讲堂" in line:
            t = line.strip()
            name = t.split(":")[1][:-1]
            # print(name)
            print(f"[{name}, {name}],")

get_name("./ais1.json")
