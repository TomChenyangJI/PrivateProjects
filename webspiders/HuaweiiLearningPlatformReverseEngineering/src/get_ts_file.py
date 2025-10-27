import requests
from get_uris import get_ts_uris
from configs import Configs, request_get

uris = get_ts_uris()
count = 0
for uri in uris:
    for config in Configs:
        print(uri)
        response = request_get(uri, config)
        print(response.status_code, type(response.status_code))
        if response.status_code == 200:
            with open(f"./ts_dir/{count}.ts", "wb") as fi:
                fi.write(response.content)
            count += 1
            break
        else:
            continue
