import time
import random
# from waitingList import waiting_courses
from multiprocessing import Pool
from configs import PROJECT_BASE_DIRECTORY


def get_response_without_headers(url):
    import requests
    response = requests.get(url)
    return response.content


def download_one_course_video(course_info_json_path=f"{PROJECT_BASE_DIRECTORY}/test_script/jsons/course_info.json",
                              parent_directory='', name_count=0):
    import time
    import random
    import os
    from vid_downloader import m3u8_video_downloader
    from course_json_parser import course_full_json_file_parser as course_json_file_parser
    from m3u8_file_downloader import download_m3u8_file
    print(" 4 -1 course_info_json_path is :", course_info_json_path)
    m3u8_file_urls = course_json_file_parser(course_info_json_path)
    # print("4 -2 m3u8_file_urls is: ", m3u8_file_urls)
    m3u8_files = []
    dir_path = f"{PROJECT_BASE_DIRECTORY}/m3u8_files/{parent_directory}"
    os.makedirs(dir_path, exist_ok=True)
    # to download the m3u8 files
    # print("4  m3u8_file_urls is: ", m3u8_file_urls)
    for url in m3u8_file_urls:
        # download the files
        name_count += 1
        output_path = f'{dir_path}/{name_count}.m3u8'
        if url.endswith(".m3u8"):
            time.sleep(2)
            response_content = get_response_without_headers(url)
            with open(output_path, "wb") as fi:
                fi.write(response_content)
                print(f"{name_count}.m3u8 has been written to m3u8_files directory")
                m3u8_files.append(output_path)
        else:
            os.makedirs(dir_path, exist_ok=True)
            time.sleep(2)
            download_m3u8_file(url, output_path)
            m3u8_files.append(output_path)
            print("The m3u8 file have been downloaded and saved to m3u8_files directory")

    # to download the videos with m3u8 files
    name_count = 0
    for url in m3u8_files:
        name_count += 1
        print("url is ", url)
        print(f"This is the {name_count}-th file which is beening downloading.")
        time.sleep(random.randint(3, 10))
        os.makedirs(
            f"{PROJECT_BASE_DIRECTORY}/videos/{parent_directory}",
            exist_ok=True)
        # prefix = url.split("/")[-1].strip()
        print(">>>> video output path is: ", f"{PROJECT_BASE_DIRECTORY}/videos/{parent_directory}/{name_count}.mp4")
        m3u8_video_downloader(url,
                              f"{PROJECT_BASE_DIRECTORY}/videos/{parent_directory}/{name_count}.mp4")


def process_function(key_val):
    dir_path = key_val[0]
    json_path = key_val[1]
    download_one_course_video(
        f"{PROJECT_BASE_DIRECTORY}/test_script/jsons/{json_path}",
        dir_path)
    print("3   json path is: ", json_path)
    time.sleep(60 * 2 + random.randint(3, 10))


# if __name__ == "__main__":
#     with Pool(5) as p:
#         p.map(process_function, waiting_courses)

"""
Decode the token or cookies generation. And create a function to update the dynamic token.
DONE!
~/src/customized_requests/get_request.py
"""

# TODO
"""
Create a github repository for this project.
"""
