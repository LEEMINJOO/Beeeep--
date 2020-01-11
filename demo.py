import os
import pandas as pd
from pytube import YouTube
from moviepy.editor import *
import librosa
import numpy as np
from keras.models import Model, load_model, Sequential
from keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from keras.layers import GRU, Bidirectional, BatchNormalization, Reshape, multiply

from td_utils import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download_url(url, type='mp4'):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension=type).order_by('resolution').last().download(filename="tmp")


def make_model(input_shape):
    X_input = Input(shape=input_shape)
    X = Conv1D(196, kernel_size=15, strides=4)(X_input) 
    X = BatchNormalization()(X) 
    X = Activation('relu')(X)
    X = Dropout(0.2)(X) 
    X = GRU(units=128, return_sequences=True)(X)
    X = BatchNormalization()(X)
    X = Dropout(0.2)(X)
    y = Activation("softmax")(X)
    X = multiply([y, X])
    X = GRU(units=128, return_sequences=True)(X)
    X = BatchNormalization()(X)
    X = Dropout(0.2)(X)
    y = Activation("softmax")(X)
    X = multiply([y, X])
    X = TimeDistributed(Dense(1, activation="sigmoid"))(X)
    model = Model(inputs=X_input, outputs=X)
    return model


def main(url, idd=0):
    download_url(url)
    print(bcolors.OKGREEN + '\nDownloaded video ! \n' + bcolors.ENDC)

    videoclip = VideoFileClip("tmp.mp4")
    audioclip = videoclip.audio
    audioclip.write_audiofile("tmp.wav")
    X = []
    X.append(np.transpose(graph_spectrogram("tmp.wav", minus=False, nfft=200, hop=80)))
    X = np.array(X)
    X = (X - X.min()) / (X.max() - X.min())
    print(bcolors.OKGREEN + '\nMade mel-spectrogram data ! ({})\n'.format(X.shape) + bcolors.ENDC)

    model = make_model(input_shape=(None, 128))
    model.load_weights("./demo/model.hdf5")
    print(bcolors.OKGREEN + '\nMade model and Loaded weight ! \n' + bcolors.ENDC)

    y = output_postprocessing(model.predict(X), 0.5)
    print(bcolors.OKGREEN + 'Finished Predict ! \n' + bcolors.ENDC)

    make_beep_wav("tmp.wav", y[0], "./demo/result_{}.wav".format(idd))
    videoclip = videoclip.set_audio(AudioFileClip("./demo/result_{}.wav".format(idd)))
    # videoclip.audio = AudioFileClip("result.wav")
    print(bcolors.OKGREEN + 'Result: shape ({}) , # of 1 ({})\n'.format(y.shape, np.count_nonzero(y)) + bcolors.ENDC)
    # Zanngu
    videoclip = videoclip.subclip(28, 34)
    # videoclip = videoclip.subclip(0, 30)
    videoclip.write_videofile("./demo/result_{}.mp4".format(idd))

    videoclip = VideoFileClip("tmp.mp4")
    videoclip = videoclip.subclip(28, 34)
    videoclip.write_videofile("./demo/origin_{}.mp4".format(idd))

    print(bcolors.OKGREEN + '\nNow you can check!!! ' + bcolors.ENDC)


if __name__ == '__main__':
    url = input('URL을 입력하세요: ')
    idd = int(input('ID: '))
    main(url, idd)

