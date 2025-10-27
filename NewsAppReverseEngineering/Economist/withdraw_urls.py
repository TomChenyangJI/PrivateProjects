from bs4 import BeautifulSoup
import json
import requests
import time
from config import *
from get_paper_body import get_body


# domain = 'https://www.economist.com'

def get_story_details(story):
    if not story:
        return None
    headline = story.get("headline", None)
    rubric = story.get("rubric", None)
    url = story.get('url', None)
    publishedDate = story.get('formattedPublishedDate', None)

    return headline, rubric, url, publishedDate


def get_first_component(res):
    soup = BeautifulSoup(res.text, features='html.parser')
    script = soup.find('script', attrs={'id': "__NEXT_DATA__"})
    d = json.loads(script.text)

    props = d.get("props")
    pageProps = props.get("pageProps")

    content = pageProps.get("content")
    components = content.get("components")
    first_component = components[0]
    return first_component

# with open("temp.html") as fi:
#     content = fi.read()
#
# soup = BeautifulSoup(content, features='html.parser')
# script = soup.find('script', attrs={'id': "__NEXT_DATA__"})
# d = json.loads(script.text)
#
# props = d.get("props")
# pageProps = props.get("pageProps")
#
# content = pageProps.get("content")
# components = content.get("components")
# first_component = components[0]


def get_leadStory(first_component):
    # first_component = get_first_component(res)
    return first_component.get('leadStory') if first_component else None

# leadStory = first_component.get('leadStory') if first_component else None
# lead story
# leadStory = first_component.get("leadStory")
# print(get_story_details(leadStory))


def get_Stories(first_component, key):
    # key: secondaryStories, tertiaryStories
    # first_component = get_first_component(res)
    return first_component.get(key) if first_component else None


# secondary stories
# secondaryStories = first_component.get("secondaryStories")
# for story in secondaryStories:
#     # print(get_story_details(story))
#     pass




# count = 0

# tertiary stories
# tertiaryStories = first_component.get("tertiaryStories")
# for story in tertiaryStories:
#     count += 1
#     # print(get_story_details(story))
#     _, _, url, _ = get_story_details(story)
#     full_url = domain + url
#
#     res = requests.get(full_url, headers=headers, cookies=cookies)
#     print(full_url, res.status_code)
#
#     with open(f"paper{count}.html", 'w') as fi:
#         fi.write(res.text)
#     time.sleep(1)


def get_story_paragraphs(story):
    _, _, url, date = get_story_details(story)
    # paras = ""
    full_url = domain + url
    res = requests.get(full_url, headers=headers, cookies=cookies)
    return get_body(res)
