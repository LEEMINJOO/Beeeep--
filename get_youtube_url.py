#!/usr/bin/env python
# coding: utf-8

# ## 유튜브 영상 url 모으기

import pandas as pd
from pytube import Playlist, YouTube

def save(links):
    df = pd.DataFrame({'links':links})
    df.to_csv('./data/urls.csv', index=False)

links = []
count = 0
main_link = "https://www.youtube.com"

playlist_urls = ['플레이리스트 링크들']

for playlist_url in playlist_urls:
    pl = Playlist(playlist_url)
    for tmp_link in pl.parse_links():
        link = main_link + tmp_link
        try: # 비공개영상 접근 불가, key error
            yt = YouTube(link) 
            links.append(link)
            count += 1
            print(count)
        except:
            print('Except')
        if count%100 == 1:
            save(links)
            print('Saved')
            
save(links)
print('Saved')
