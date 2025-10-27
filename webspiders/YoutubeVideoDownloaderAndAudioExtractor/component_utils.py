

def get_video_list(path="./video_list.txt"):
    with open(path, "r") as fi:
        lines = fi.readlines()
        lines = [line.strip() for line in lines]
        return lines