import os

import requests
from config import *
import json
import re
import asyncio
from googletrans import Translator
from get_job_ids_from_one_response import get_job_ids_from_one_response


def out_wrapper(func):
    def wrapper(content):
        result = asyncio.run(func(content))
        return result
    return wrapper


@out_wrapper
async def translate_content(content) -> str:
    async with Translator() as translator:
        translations = await translator.translate(content, dest='en')
        return translations.text


def get_entries_in_page(page) -> requests.Response:
    response = requests.get(
        f"https://www.linkedin.com/voyager/api/graphql?queryId=voyagerJobsDashJobCards.bef088d2745c26e5851c152103cb2bd2",
        cookies=cookies,
        headers=headers,
    )
    with open(f"../pages/{page}.json", "w") as fi:
        fi.write(response.text)

    return response


def get_job_title(json_obj):
    title = json_obj['data']['title']
    return title


def get_jd(json_obj):
    # get_jd from json file, other than sending request to Linkedin server
    jd = json_obj['data']['description']['text']
    return jd


def get_job_description(job_id) -> requests.Response:
    # this method is used to get the job description with the job id as part of the request url
    response = requests.get(
        f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_id}',
        cookies=cookies,
        headers=headers,
    )
    return response


def language_filter(text: str):
    target = ""
    with_language = False
    lower_text = text.lower()
    if "german" in lower_text:
        i = lower_text.index("german")
        l = len(text)
        if 10 <= i <= l - 20:
            target = text[i-10: i + 20]
        else:
            end_i = l if i + 5 > l else i + 5
            target = text[i: end_i]
    if target != "" and "germany" not in target.lower():
        text = "Language requirements: " + target + "\n" + text
        with_language = True
    return text, with_language


def translate_title_and_jd(res_job_description, job_id):
    # https://www.linkedin.com/jobs/search/?currentJobId=4108121326
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

    with open(f"{job_descriptions_en}/{file_name}", "w") as out_fi:
        content_en = "\n" + job_url + "\n\n" + title_en + "\n\n" + jd_en
        out_fi.write(content_en)
    # ----- translate work done -----


def convert_txt_to_pdf(in_file, file):
    os.makedirs("../job_descriptions_pdf/german/", exist_ok=True)
    # text file to pdf file
    from fpdf import FPDF

    # Open the text file and read its contents
    with open(in_file, 'r') as f:
        text = f.read()
        # text = language_filter(text)
    text, with_language = language_filter(text)
    if with_language:
        out_file = f"../job_descriptions_pdf/german/{file.replace('txt', 'pdf')}"
    else:
        out_file = f"../job_descriptions_pdf/{file.replace('txt', 'pdf')}"
    pdf = FPDF()
    pdf.add_font('Times', '', "Times New Roman.ttf", uni=True)

    # Add a new page to the PDF
    pdf.add_page()
    # Set the font and font size
    pdf.set_font('Times', size=12)

    # Write the text to the PDF
    pdf.write(5, text)

    # Save the PDF
    pdf.output(out_file)


def copy_files_to_another_folder(in_file, trg_foler="../job_descriptions_pdf/mannual_intervene/"):
    import shutil
    file_name = in_file.split("/")[-1]
    shutil.copyfile(in_file, trg_foler + file_name)

