import requests

cookies = {
}

headers = {
    'Host': 'abc.xxxxxx.com',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Sec-Fetch-Mode': 'no-cors',
    'Accept': '*/*',
    'Referer': 'https://abc.xxxxxx.com/',
    'Sec-Fetch-Dest': 'video',
}

response = requests.get(
    'https://abc.xxxxxx.com/xxxxxxx/ProxyForDownLoad/iMSS_Video/play/8af4d2358d1c6679018d49ae62bf4e5b/8af4d2358d1c6679018d49ae62d74e5c/28.m3u8',
    cookies=cookies,
    headers=headers,
)

print(response)
print('-' * 50)
print(response.content)
print('*' * 50)
with open("urls_xxxxxx.txt", "w") as fl:
    fl.write(response.text)
print(response.text)
print("&" * 50)
print(response.links)
print("^" * 50)

