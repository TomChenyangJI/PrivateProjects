import os
from component_utils import get_courses, get_frame
from config import base_dir


# courses = os.listdir(base_dir)
# courses = [os.path.join(base_dir, course) for course in courses]
# print(courses)


# courses, abs_paths = get_courses(base_dir)
courses = get_courses(base_dir)
for course in courses:
    print(course)


for course in courses:
    if course != ".DS_Store" and course != "readme.txt":
        abs_path = os.path.join(base_dir, course)
        vids = os.listdir(abs_path)
        vids = [os.path.join(abs_path, vid) for vid in vids]
        # print(course)
        amount = 0
        t_li = [1, 3, 5, 7, 10, 15]
        os.makedirs(f"./screen_shots/{course}", exist_ok=True)
        for vid in vids:
            try:
                for t in t_li:
                    amount += 1
                    get_frame(vid, t, f"./screen_shots/{course}/{amount}.png")
            except IOError:
                continue




