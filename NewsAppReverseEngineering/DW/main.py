from pyquery import PyQuery as pq

with open("test.html", 'r') as fi:
    content = fi.read()

d = pq(content)
print(d("#root > div.lgl2mqt.livgtmk > div:nth-child(5) > div.c8dev6m.container-fluid > section:nth-child(2) > div > article > div > header > p").text())