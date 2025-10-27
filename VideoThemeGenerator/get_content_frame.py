from moviepy.editor import VideoFileClip


vid_path = "./oridinary_vids/2.mp4"

clip = VideoFileClip(vid_path)
clip.save_frame("test.png", t=50)  # IOError