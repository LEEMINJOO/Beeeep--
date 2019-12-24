# Beeeep--

## 투빅스 9회 컨퍼런스 준비

#### 폴더경로

./data

./data/video
- blahblah.mp4
  
./data/audio
- blahblah.wav
- blahblah_0.wav

./data/text
- blahblah.txt

#### process

1224: prototype코드 작성
* get_youtube_url.py - 플레이 리스트 링크로 전체 url 크롤링
* urls_to_video.py - url 리스트를 읽어와 video 저장
* video_to_text_outloop.ipython - **video_to_test.py와 연결해야함**
* video_to_audio.py - 비디오를 오디오로 변환 후 자막 기반으로 clip하고 labeling

 
