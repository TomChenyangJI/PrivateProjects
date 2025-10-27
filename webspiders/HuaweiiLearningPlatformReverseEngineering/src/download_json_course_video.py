from configs import PROJECT_BASE_DIRECTORY


def download_one_json_video(course_info_json_path=f"{PROJECT_BASE_DIRECTORY}/test_script/jsons/course_info.json",
                              directory_count=0, name_count=0):
    import time
    import random
    import os
    from vid_downloader import m3u8_video_downloader
    from course_json_parser import course_json_file_parser
    from m3u8_file_downloader import download_m3u8_file

    m3u8_file_urls = course_json_file_parser(course_info_json_path)
    m3u8_files = []
    dir_path = f"{PROJECT_BASE_DIRECTORY}/m3u8_files/{directory_count}"

    # to download the m3u8 files
    for url in m3u8_file_urls:
        # download the files
        name_count += 1
        os.makedirs(dir_path, exist_ok=True)
        time.sleep(1)
        output_path = f'{dir_path}/{name_count}.m3u8'
        download_m3u8_file(url, output_path)
        m3u8_files.append(output_path)
        print("The m3u8 file have been downloaded and saved to m3u8_files directory")

    # to download the videos with m3u8 files
    for url in m3u8_files:
        print("url is ", url)
        print(f"This is the {name_count}-th file which is beening downloading.")
        time.sleep(random.randint(3, 10))
        name_count += 1
        os.makedirs(
            f"{PROJECT_BASE_DIRECTORY}/videos/{directory_count}",
            exist_ok=True)
        m3u8_video_downloader(url,
                              f"{PROJECT_BASE_DIRECTORY}/videos/{directory_count}/{name_count}.mp4")


