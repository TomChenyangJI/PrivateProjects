import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

headers = {
}

response = requests.get(
    'https://sspevent.dzh.com.cn/',
    headers=headers,
    verify=False,
)
with open("file.gif", 'wb') as fi:
    fi.write(response.content)
print(response.status_code)