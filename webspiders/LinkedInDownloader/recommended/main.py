import requests
import time
from config import cookies, headers
from components import get_job_ids_from_one_response, get_job_description, get_job_title, translate_title_and_jd
from content_translator import translate_content

def get_entries_in_page(page) -> requests.Response:
    response = requests.get(
        f'https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?start={25*page}',
        cookies=cookies,
        headers=headers,
    )

    with open(f"pages/{page}.json", "w") as fi:
        fi.write(response.text)

    return response


if __name__ == "__main__":
    init_page = 0
    trial = 0
    while True:
        try:
            for page in range(init_page, 2000):
                init_page = page
                print("***  page number is : ", page)
                res = get_entries_in_page(page)
                job_ids = get_job_ids_from_one_response(res.text)
                print("\t", job_ids)
                for job_id in job_ids:
                    time.sleep(10)
                    res_job_description = get_job_description(job_id)
                    with open(f"job_descriptions/{job_id}.json", "w") as jb_out:
                        jb_out.write(res_job_description.text)
                        print("\t\t> job_id is: ", job_id)

                    # translate the title and jd
                    translate_title_and_jd(res_job_description, job_id)

                time.sleep(30)

        except Exception as e:
            trial += 1
            print(f"this is the {trial}-th time encountering exception")
            print("\t", e)
            time.sleep(120)
        else:
            break


#  how to tokenize the input
