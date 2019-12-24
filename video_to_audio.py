#!/usr/bin/env python
# coding: utf-8

# ## video audio 저장

import os
import pandas as pd
from moviepy.editor import *

def make_dir(dir_):
    if not os.path.isdir(dir_):
        os.mkdir(dir_)

def change_dir(from_dir, before='video', after='audio'):
    if after == 'audio':
        type_ = '.wav'
    elif after == 'text':
        type_ = '.txt'
    
    to_dir = from_dir.split('/')
    to_dir[-2] = after
    to_dir[-1] = to_dir[-1].split('.')[0] + type_
    return os.path.join(*to_dir)

def video_to_audio(video_dir):
    audio_dir = change_dir(video_dir, before='video', after='audio')
    print(video_dir)
    audioclip = VideoFileClip(video_dir).audio
    audioclip.write_audiofile(audio_dir)
    return audio_dir

def clip_audio(audio_dir):
    total = pd.DataFrame(columns=['audio','text', 'length'])
    
    text_dir = change_dir(audio_dir, before='audio_dir', after='text')
    
    df = pd.read_csv(text_dir, header=None, sep='\t')
    df.columns = ['time', 'text']
    
    for i in range(len(df)):
        full_audio = AudioFileClip(audio_dir)
        full_time = int(full_audio.end)
        
        tmp_dir = audio_dir[:-4] + '_{}.wav'.format(i)
        start_time = pd.Timedelta(df['time'][i]).total_seconds()
        if i != (len(df)-1):
            end_time = pd.Timedelta(df['time'][i+1]).total_seconds()
        else:
            end_time = full_time

        tmp_audio = full_audio.subclip(start_time, end_time)
        tmp_audio.write_audiofile(tmp_dir)
        
        total = total.append({'audio':tmp_dir, 
                              'text':df['text'][i], 
                              'length':(end_time-start_time)}, ignore_index=True)
    
    return total

def labeling(df):
    labels = []
    for i, row in df.iterrows():
        print('Text:', row['text'])
        l = int(input('Label: '))
        labels.append(l)
    labels = pd.DataFrame({'labels':labels})
    return df.join(labels)

if __name__ == '__main__':
    audio_dir = os.path.join('.','data','audio')
    make_dir(audio_dir)

    df = pd.read_csv(os.path.join('.', 'data', 'links_videos.txt'))
    result = pd.DataFrame(columns=['audio', 'text', 'length', 'label'])

    for _, row in df.iterrows():
        video_dir = row['videos']
        audio_dir = video_to_audio(video_dir)
        clip_df = clip_audio(audio_dir)
        labeling_df = labeling(clip_df)
        result = result.append(labeling_df, ignore_index=True)
