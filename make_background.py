from moviepy.editor import *
import os

def make_one_background_wav(sound, start_time=0, end_time=10):
    return sound.subclip(start_time, end_time)

def read_sound(path):
    audioclip = AudioFileClip(path)
    audio_list = [audioclip for i in range(10)]
    ret_clip = concatenate_audioclips(audio_list)
    return ret_clip


def save_sound(name, audioclip, new_dir):
    new_path = os.path.join(new_dir, name)
    audioclip.write_audiofile(new_path)

data_path = os.path.join(".","data","background")
new_dir_path = os.path.join(".", "data", "new_background")
os.makedirs(new_dir_path, exist_ok=True)

names = os.listdir(data_path)
# print(names)
# print(new_dir_path)

for name in names:
    one_path = os.path.join(data_path, name)
    sound = read_sound(one_path)
    sound = make_one_background_wav(sound)
    save_sound(name, sound, new_dir_path)
