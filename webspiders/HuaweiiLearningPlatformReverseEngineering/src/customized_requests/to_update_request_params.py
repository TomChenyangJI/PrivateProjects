import requests

cookies = {
}

headers = {
}

data = 'QbyeURcHZY3d0%3D&publicKeyFlag=0'


def first_request():
    global cookies, headers, data
    response = requests.post(
        'https://abc.xxxxxx.com/xxxxxxx/LoginWithSF',
        # 'https://image.xxxxxx.com/tiny-lts/v1/images/6edd41eba9032d846862bf49ef01cbef_628x1280--org.png',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False
    )
    response_cookies = response.cookies
    # print(response.cookies)
    # print(response_cookies.keys())
    for key, val in response_cookies.items():
        print(f"'{key}': '{val}',")
        cookies[key] = val


def save_cookies_to_json(cookies, output_path="./cookies.json"):
    with open(output_path, "w") as fi:
        import json
        serialized_str = json.dumps(cookies)
        fi.write(serialized_str)


def get_and_save_new_cookies(output_path="./cookies.json"):
    first_request()
    save_cookies_to_json(cookies, output_path)
