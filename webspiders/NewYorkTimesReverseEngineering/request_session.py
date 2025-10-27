import requests


# s = requests.session()
# s.get("https://www.nytimes.com/", verify=False)

def NYTSession(url="https://www.nytimes.com/"):
    with requests.session() as s:
        s = requests.session()
        response = s.get(url, verify=False)
        headers = response.headers
        cookies = headers.get("Set-Cookie")
        headers["cookie"] = cookies
        headers.pop("Set-Cookie")
        print(headers)
        print(">>>><<<<")
        response = s.get("https://www.nytimes.com/2024/06/23/world/europe/the-nation-resurgent-and-borders-too.html",
        # headers=headers,
                         verify=False)
        print(response.status_code)


NYTSession()

