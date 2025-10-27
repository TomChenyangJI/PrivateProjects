import json
import re


def get_job_ids_from_one_response(res: str):
    js_obj = json.loads(res)
    # with open("temp.html", "w") as te:
    #     te.write(res)

    elements = js_obj["data"]["data"]["jobsDashJobCardsByJobCollections"]["elements"]

    job_ids = []

    for ele in elements:
        jobPostingCard = ele.get("jobCard").get("*jobPostingCard")
        job_id = re.search("\d{10}", jobPostingCard)
        job_id = job_id.group(0)
        job_ids.append(job_id)

    print(job_ids)
    return job_ids


with open("../pages/0.json", "r") as fi:
    content = fi.read()
    job_ids = get_job_ids_from_one_response(content)
    print(job_ids)