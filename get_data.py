from utils import make_dir, save_playlist_links, save_videos, save_audios, labeling, wave_to_image

import os
import argparse
import pandas as pd

chrome_dir = './chromedriver.exe'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--get_links", default=False, action="store_true")
    parser.add_argument("--get_videos", default=False, action="store_true")
    parser.add_argument("--get_texts", default=False, action="store_true")
    parser.add_argument("--get_audios", default=False, action="store_true")
    parser.add_argument("--labeling", default=False, action="store_true")
    parser.add_argument("--get_images", default=False, action="store_true")
    args = parser.parse_args()

    links_dir = os.path.join(".", "data", "links.csv")
    links_videos_dir = os.path.join('.', 'data', 'links_videos.txt')
    links_videos_texts_dir = os.path.join('.','data','links_videos_texts.txt')
    audios_texts_length_dir = os.path.join('.', 'data', "audios_texts_length_labels.csv")

    if args.get_links:
        print('Get Links')
        playlist_urls = ['링크들']
        save_playlist_links(playlist_urls, links_dir)

    if args.get_videos:
        print('Get Videos')
        video_dir = os.path.join('.','data','video')
        make_dir(video_dir)
        df = pd.read_csv(links_dir)
        save_videos(df, links_videos_dir)

    if args.get_texts:
        from crawling import crawling
        print('Get Texts')
        text_dir = os.path.join('.','data','text')
        make_dir(text_dir)
        df = pd.read_csv(links_videos_dir)
        crawling(df, chrome_dir, links_videos_texts_dir)

    if args.get_audios:
        print('Get Audios')
        audio_dir = os.path.join('.','data','audio')
        make_dir(audio_dir)       
        df = pd.read_csv(links_videos_texts_dir)
        save_audios(df, audios_texts_length_dir)

    if args.labeling:
        print('Labeling')
        df = pd.read_csv(audios_texts_length_dir, encoding='ms949')
        labeling(df, audios_texts_length_dir)
    
    if args.get_images:
        print('Get Images')
        wave_to_image(audios_texts_length_dir)
        