import time

import requests
from config import *
from withdraw_urls import *

response = requests.get('https://www.economist.com/', cookies=cookies, headers=headers)
# with open("temp.html", "w") as fi:
#     fi.write(response.text)

first_component = get_first_component(response)
leadStory = get_leadStory(first_component)
secondaryStories = get_Stories(first_component, 'secondaryStories')
tertiaryStories = get_Stories(first_component, 'tertiaryStories')


lead_story_paras = get_story_paragraphs(leadStory)
# here is the entry I could list on the webpage
lead_story_details = get_story_details(leadStory)  # headline, rubric, url, publishedDate

for story in secondaryStories:
    paragraphs = get_story_paragraphs(story)
    print(paragraphs)
    time.sleep(0.5)

for story in tertiaryStories:
    paragraphs = get_story_paragraphs(story)
    print(paragraphs)
    time.sleep(0.5)

# TODO do not forget to solve the connection error,
#  I need to request a few times
