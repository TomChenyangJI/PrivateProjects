def download_m3u8_file(
        uri="https://imss-video.xxxxxx.com/video/play/873928258617a9b10186d9af0fe348b6/873928258617a9b10186d9af0ffa48b7/28.m3u8", \
        output_path="test2_m3u8.m3u8"):
    from web_spider_test.image_downloader.src import configs
    cfg = configs.__dict__
    for key, val in cfg.items():
        if key.startswith("config"):
            response = cfg.get('request_get')(
                uri, val)
            if response.status_code == 200:
                with open(output_path, "wb") as fi:
                    fi.write(response.content)
                print(f"{uri} has been downloaded!")
                break
            else:
                print(response.status_code, " is the status code.")
