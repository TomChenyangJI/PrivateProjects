import requests

cookies = {
}

headers = {
}

data = {
    'debug': 'true',
    'log': '[{}]',
}

response = requests.get('https://video.twimg.com/amplify_video/1887238808250257408/pl/jF6tL3TfRYacobqa.m3u8?tag=14&v=2b8', cookies=cookies, headers=headers, verify=False)


import json

with open('temp.m3u8', 'w') as fi:
    print(response.text)
    fi.write(response.text)
