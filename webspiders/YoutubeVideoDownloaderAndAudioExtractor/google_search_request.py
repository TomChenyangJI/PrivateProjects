import requests


response = requests.get("https://www.google.com/search?q=hello")

# response = requests.get("https://www.reddit.com/user/chevignon93/", verify=False)
with open("test/test.txt", "wb") as fi:
    fi.write(response.content)