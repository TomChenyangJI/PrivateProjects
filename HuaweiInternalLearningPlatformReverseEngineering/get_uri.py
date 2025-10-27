

with open("./urls_xxxxxx.txt", 'r') as fi:
    lines = fi.readlines()

urls = []
for line in lines:
    if line.startswith("http"):
        urls.append(line.strip())

import requests


for url in urls:
    response = requests.get(url)
    component = url.split("/")
    name = component[-1]
    with open(f"./videos/{name}", "wb") as vid:
        vid.write(response.content)
