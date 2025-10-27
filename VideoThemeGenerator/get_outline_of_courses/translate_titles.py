from component_utils import translate_sentence, get_courses
from config import base_dir


courses = get_courses(base_dir)

content = ""
amount = 0
for course in courses:
    amount += 1
    title_en = translate_sentence(course, "en")

    content_component = f"{amount}. {course}, {title_en}\n"
    content += content_component
    print(content_component)

with open("courses.txt", "w") as out_fi:
    out_fi.write(content)

"""
The part before `, ` is the original title of the course, while the part behind it is the English title translated by
Google Translate, by calling its api. 
I also checked it for myself, I found the accuracy was high, therefore, I didn't make a change on them.
"""