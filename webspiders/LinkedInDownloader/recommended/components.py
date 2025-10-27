import json
import re
from config import cookies, headers
import requests
from content_translator import translate_content


def get_job_title(json_obj):
    title = json_obj['data']['title']
    return title


def get_jd(json_obj):
    # get_jd from json file, other than sending request to Linkedin server
    jd = json_obj['data']['description']['text']
    return jd


def get_job_ids_from_one_response(res: str):
    js_obj = json.loads(res)
    # with open("temp.html", "w") as te:
    #     te.write(res)
    jobCardPrefetchQueries = js_obj["data"]["metadata"]["jobCardPrefetchQueries"]
    first_ele = jobCardPrefetchQueries[0]
    prefetchJobPostingCard = first_ele["prefetchJobPostingCard"]
    job_cards = prefetchJobPostingCard.keys()

    job_ids = []

    for job_card in job_cards:
        result = re.search("\d{10}", job_card)
        job_id = result.group(0)
        job_ids.append(job_id)

    return job_ids


def get_job_description(job_id) -> requests.Response:
    # this method is used to get the job description with the job id as part of the request url
    response = requests.get(
        f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_id}',
        cookies=cookies,
        headers=headers,
    )

    return response


def translate_title_and_jd(res_job_description, job_id):
    # https://www.linkedin.com/jobs/search/
    # translate the title and jd
    if isinstance(res_job_description, requests.Response):
        json_obj = res_job_description.json()
    elif isinstance(res_job_description, dict):
        json_obj = res_job_description

    title = get_job_title(json_obj)
    jd = get_jd(json_obj)
    title_en = translate_content(title)
    jd_en = translate_content(jd)
    jd_en = "\n\n" + jd_en
    file_name = job_id + "-" + title_en + ".txt"
    file_name = file_name.replace("/", "|")
    job_url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}"

    with open(f"job_descriptions_en/{file_name}", "w") as out_fi:
        content_en = "\n" + job_url + "\n\n" + title_en + "\n\n" + jd_en
        out_fi.write(content_en)
    # ----- translate work done -----