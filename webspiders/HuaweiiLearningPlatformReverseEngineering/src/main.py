from video_downloader import process_function
from multiprocessing import Pool
from waitingList import waiting_courses

if __name__ == "__main__":
    with Pool(5) as p:
        p.map(process_function, waiting_courses)
