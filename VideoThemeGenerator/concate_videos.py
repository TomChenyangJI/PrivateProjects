from moviepy.editor import VideoFileClip, concatenate_videoclips


def get_video_list(collection_path):
    """
    This function is used to read the video paths saved in the file `collection_path`
    :param collection_path: a file path, in which the video paths have been saved
    :return: a list with video paths
    """
    with open("video_list.txt", "r") as infile:
        videos = infile.readlines()
        videos = [vid.strip() for vid in videos]
    return videos


video_list = get_video_list("./video_list.txt")

clip_obj_list = []

# Load the video clips
for vid in video_list:
    temp_clip = VideoFileClip(vid)
    clip_obj_list.append(temp_clip)
    # print(temp_clip.audio)

# Concatenate the video clips
final_clip = concatenate_videoclips(clip_obj_list, method='chain')
final_clip.save_frame("poster.png")

# Write the final video to a file
final_clip.write_videofile("output.mp4")
# here I have comment out the line on 94 in file `/python3.11/site-packages/moviepy/video/io/ffmpeg_writer.py`
# because with this line, the generated video is with no audio