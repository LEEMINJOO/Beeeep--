# Beeeep--; 투빅스 9회 컨퍼런스 준비

## 코드

* 유튜브에서 음성 얻기
- get_data.py

* 레이블링 기준으로 배경, 활성화, 그외 음성 나누기
- audio_label_cliping.ipynb

* 음성 합치고, train data 만들기
- make_train_by_overlay.ipynb

* 학습
- Trigger word detection.ipynb

## 폴더경로

./data

./data/video
- blahblah.mp4
  
./data/audio
- blahblah.wav
- blahblah_0.wav

./data/text
- blahblah.txt

./data/label
- blahblah_0.txt
- blahblah_0.wav

./data/audio_label_clip
- background_0.xav
- negative_0.wav
- positive_0.wav

./data/train_audios
- mix_0.wav

./data/XY_train
- x_0.npy
- y_0.npy

### ref
https://github.com/Tony607/Keras-Trigger-Word
