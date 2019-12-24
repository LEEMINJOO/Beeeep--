#!/usr/bin/env python
# coding: utf-8

# ## 비디오 저장

import os
import pandas as pd
from pytube import YouTube

def make_dir(dir_):
    if not os.path.isdir(dir_):
        os.mkdir(dir_)

def link_save(link):
    yt = YouTube(link)
    video_name = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first().download()
    re_name = os.path.join(video_dir, link.split('v=')[-1]+'.mp4')
    os.rename(video_name, re_name)
    return re_name


if __name__ == '__main__':
    video_dir = os.path.join('.','data','video')
    make_dir(video_dir)

    df = pd.read_csv(os.path.join('.', 'data', 'links.csv'))
    save_file = os.path.join('.', 'data', 'links_videos.txt')
    count = 0

    with open(save_file, 'a') as f:
        f.write('links,videos\n')

    for link in set(df.links):
        try: # 접근불가 영상
            name = link_save(link)
            with open(save_file, 'a') as f:
                f.write('{},{}\n'.format(link, name))
            count += 1
            print(count)
        except:
            print('Except')
