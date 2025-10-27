import m3u8


def get_ts_uris(master_path="./temp.m3u8"):
    file = m3u8.load(master_path)
    # for key, val in file.data.items():
    #     if val:
    #         print(key, val)

    content = file.data
    uris = []
    for ele in content.get("segments"):
        # print(ele.get("uri"))
        uris.append(ele.get("uri"))
    return uris


