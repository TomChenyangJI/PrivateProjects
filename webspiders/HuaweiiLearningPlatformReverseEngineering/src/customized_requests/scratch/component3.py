import requests

proxies = {
    'http': 'http://localhost:9090',
    'https': 'http://localhost:9090',
}

cookies = {
}

headers = {
}

response = requests.get(
    'https://abc.xxxxxx.com/xxxxxxx/ProxyForImage/tinyimage_lts_org/v1/images/18c07bb76c2f258102dab5e1f604503a_1080x356.png',
    cookies=cookies,
    headers=headers,
    verify=False
)
print(response.headers)
print("*" * 40)

print(response.cookies)
print(response.content)