import json
from bs4 import BeautifulSoup


def get_body(res):
    soup = BeautifulSoup(res.text, features='html.parser')
    script = soup.find("script", attrs={"id": "__NEXT_DATA__"})
    d = json.loads(script.text)
    body = d.get('props').get('pageProps').get('content').get('body')
    body_txt = ""
    for ele in body:
        if ele.get('type') == "PARAGRAPH":
            txt = ele.get("text").strip()
            body_txt += txt + "\n"
    return body_txt

# with open("paper1.html") as fi:
#     content = fi.read()

# soup = BeautifulSoup(content, features='html.parser')
# script = soup.find("script", attrs={"id": "__NEXT_DATA__"})
# d = json.loads(script.text)
# body = d.get('props').get('pageProps').get('content').get('body')
# body_txt = ""
# for ele in body:
#     if ele.get('type') == "PARAGRAPH":
#         txt = ele.get("text").strip()
#         body_txt += txt + "\n"
# print(body_txt)


