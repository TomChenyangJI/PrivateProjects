from pytube import YouTube
from pytube.innertube import _default_clients
from extract_audio_from_video import extract_audio_customized
from component_utils import get_video_list
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]



vid_title = ""


def format_vid_title(vid_title=vid_title):
    # global vid_title
    if " " in vid_title:
        vid_title = vid_title.strip().replace(" ", "")
    if "/" in vid_title:
        vid_title = vid_title.replace("/", "")
    return vid_title


# Function to download YouTube video
def download_youtube_video(url, output_path='.', recu=0):
    global vid_title
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url,
                     use_oauth=False,
                     allow_oauth_cache=True
                     )
        # Print video title
        print(f"Title: {yt.title}")
        vid_title = yt.title
        vid_title = format_vid_title(yt.title)

        # Get the highest resolution stream
        ys = yt.streams.get_highest_resolution()

        # Print the download start message
        print("Downloading...")

        # Download the video
        output_path += "/mp4"
        print(f"\toutput path is: {output_path}", f"filename is : {vid_title + '.mp4'}")
        ys.download(output_path, filename= vid_title + ".mp4")

        # Print download completion message
        print("Download completed!")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)
        print("Download again!")
        if recu > 3:
            pass
        else:
            download_youtube_video(url, output_path, recu+1)


def get_audio_path(vid_path: str):
    # i = vid_path.rfind(".")
    return vid_path + ".mp3"


def download_music():
    """
    remember this function also downloads video
    :return:
    """
    video_list = get_video_list()
    for video_url in video_list:
        # vid_output_path = "./"
        # video_url = 'https://www.youtube.com/watch?v=raHLFg6bkNI'  # Replace with your video URL
        download_youtube_video(video_url)
        # extrac the audio from the video
        print("\nExtracting the audio from the video ...")
        aud_input_path = vid_title
        aud_output_path = get_audio_path(aud_input_path)
        # print("audio path: ", aud_output_path)
        aud_input_path = "./mp4/" + vid_title + ".mp4"
        try:
            extract_audio_customized(aud_input_path, "./mp3/" + aud_output_path)  # this is to extract audio from the video
        except Exception as e:
            print(e)
        time.sleep(2)


def download_video_compound():
    global vid_title
    def my_video_download(url, output_path='~/PythonWorkspaces/Space1/web_spider_test/yt_test/video_audio_merge'):
        try:
            # Create a YouTube object with the URL
            yt = YouTube(url,
                         use_oauth=False,
                         allow_oauth_cache=True
                         )

            # Print video title
            print(f"Title: {yt.title}")
            vid_title = format_vid_title(yt.title)

            # Get the highest resolution stream
            # ys = yt.streams.get_highest_resolution()
            ys_video = yt.streams.get_highest_video_without_audio()
            ys_audio = yt.streams.get_audio_only()
            print("ys_video >> :", ys_video)
            print("ys_audio ** :", ys_audio)

            # Print the download start message
            print("Downloading...")

            # Download the video
            # ys_video.download(output_path, filename="mp4/" + vid_title + ".mp4")
            # ys_audio.download(output_path, filename="mp3/" + vid_title + ".mp3")
            import threading
            t1 = threading.Thread(target=ys_video.download, args=(output_path, "mp4/" + vid_title + ".mp4"))
            t2 = threading.Thread(target=ys_audio.download, args=(output_path, "mp3/" + vid_title + ".mp3"))
            t1.start()
            t2.start()
            t1.join()
            t2.join()


            # Print download completion message
            print("Download completed!")
        except Exception as e:
            print(f"Error: {e}")
            print("Download again!")
            my_video_download(url, output_path)

    video_list = get_video_list()

    for video_url in video_list:
        my_video_download(video_url)
        print("<>Episode Done!<>")
        time.sleep(2)

def download_video_directly():
    video_list = get_video_list()
    for video_url in video_list:
        download_youtube_video(video_url)
        print("\tEpisode Done!")
        time.sleep(2)


# Example usage
# move this part to statistics.py
# if __name__ == "__main__":
#     video_list = get_video_list()
#     for video_url in video_list:
#         # vid_output_path = "./"
#         # video_url = 'https://www.youtube.com/watch?v=raHLFg6bkNI'  # Replace with your video URL
#         download_youtube_video(video_url)
#         # extrac the audio from the video
#         print("\nExtracting the audio from the video ...")
#         aud_input_path = vid_title
#         aud_output_path = get_audio_path(aud_input_path)
#         # print("audio path: ", aud_output_path)
#         aud_input_path = "./mp4/" + vid_title + ".mp4"
#         extract_audio_customized(aud_input_path, "./mp3/" + aud_output_path)  # this is to extract audio from the video
#         time.sleep(0.5)



# TODO
# pack up the youtube downloader and audio extractor to an executable program.


# run the functions from temp0.py
# it has been commented the entry of the program

