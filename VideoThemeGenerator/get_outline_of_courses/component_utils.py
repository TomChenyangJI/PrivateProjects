import os
from googletrans import Translator
from moviepy.editor import VideoFileClip
import pytesseract  # this module doesn't work very well, it cannot extract Chinese chars on the image correctly
from PIL import Image


# TODO I may need to build a model to extract Chinese chars on the image to improve the accuracy,
#  bc currently this model doesn't work very well
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="chi_sim")
    return text


def get_frame(vid_path, t, frame_path):
    clip = VideoFileClip(vid_path)
    clip.save_frame(frame_path, t=t)


def get_vid_len(vid_path):
    clip = VideoFileClip(vid_path)
    return clip.duration


def translate_sentence(sen, dest_lan):
    translator = Translator()
    result = translator.translate(sen, dest=dest_lan)
    return result.text


def get_courses(dir):
    courses = os.listdir(dir)
    # abs_paths = [os.path.join(base_dir, course) for course in courses]
    # return courses, abs_paths
    return courses

