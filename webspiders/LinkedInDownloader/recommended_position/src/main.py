import os
from config import *
from component import *
import time


if __name__ == "__main__":
    init_page = 0
    trial = 0
    # job_description_json = "../job_description_json"
    # os.makedirs(job_description_json, exist_ok=True)
    signal = True
    while signal:
        try:
            for page in range(init_page, 2000):
                print("page: ", page)
                init_page = page
                res = get_entries_in_page(page)
                job_ids = get_job_ids_from_one_response(res.text)
                print("\t", job_ids)
                if len(job_ids) == 0:
                    signal = False
                    break
                for job_id in job_ids:
                    time.sleep(10)
                    res_job_description = get_job_description(job_id)
                    with open(f"{job_description_json}/{job_id}.json", "w") as jb_out:
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
