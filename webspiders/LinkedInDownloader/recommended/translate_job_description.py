import json
import os
import time
import re
from content_translator import translate_content
from components import get_job_title, get_jd, translate_title_and_jd


if __name__ == "__main__":
    sub_files = os.listdir("job_descriptions")

    for file in sub_files:
        if os.path.isfile(f"./job_descriptions/{file}"):
            print(file)
            jd_id = re.search("\d{10}", file)
            jd_id = jd_id.group(0)

            with open(f"./job_descriptions/{file}", "r") as in_fi:
                json_obj = json.load(in_fi)
                translate_title_and_jd(json_obj, jd_id)

            time.sleep(2)
